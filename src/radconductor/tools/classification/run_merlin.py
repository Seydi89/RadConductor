import csv
from pathlib import Path
from typing import Any, Literal

from radconductor.domain.models import (
    MerlinPhenotypeResult,
    PhenotypePrediction,
)


DevicePreference = Literal["auto", "cpu", "cuda", "mps"]


def run_merlin_phenotype_classification(
    input_path: Path,
    labels_path: Path,
    cache_directory: Path,
    top_k: int = 5,
    device: DevicePreference = "auto",
    allow_cpu_fallback: bool = True,
) -> MerlinPhenotypeResult:
    """Return Merlin's top phenotype predictions for one CT volume.

    This is a research integration and must not be used as a diagnostic result.
    """

    _validate_inputs(
        input_path=input_path,
        labels_path=labels_path,
        top_k=top_k,
    )

    try:
        import torch
        from merlin import Merlin
        from merlin.data import DataLoader
    except ImportError as exc:
        raise RuntimeError(
            "Merlin support is not installed. "
            'Install it with: pip install -e ".[merlin]"'
        ) from exc

    labels = _load_phenotype_labels(labels_path)
    cache_directory.mkdir(parents=True, exist_ok=True)

    dataloader = DataLoader(
        datalist=[
            {
                "image": str(input_path),
                "text": "",
            }
        ],
        cache_dir=str(cache_directory),
        batchsize=1,
        shuffle=False,
        num_workers=0,
    )

    try:
        batch = next(iter(dataloader))
    except StopIteration as exc:
        raise RuntimeError("Merlin produced no input batch") from exc

    selected_device = _resolve_device(
        torch=torch,
        requested=device,
    )

    model = Merlin(PhenotypeCls=True)
    model.eval()

    try:
        probabilities = _run_inference(
            torch=torch,
            model=model,
            image=batch["image"],
            device=selected_device,
        )
    except RuntimeError:
        if selected_device != "mps" or not allow_cpu_fallback:
            raise

        selected_device = "cpu"
        probabilities = _run_inference(
            torch=torch,
            model=model,
            image=batch["image"],
            device=selected_device,
        )

    if len(probabilities) != len(labels):
        raise RuntimeError(
            "Merlin output and phenotype labels have different lengths: "
            f"{len(probabilities)} predictions and {len(labels)} labels"
        )

    ranked_indices = sorted(
        range(len(probabilities)),
        key=probabilities.__getitem__,
        reverse=True,
    )[:top_k]

    predictions = tuple(
        PhenotypePrediction(
            phecode=labels[index][0],
            description=labels[index][1],
            probability=probabilities[index],
        )
        for index in ranked_indices
    )

    return MerlinPhenotypeResult(
        input_path=input_path,
        device=selected_device,
        predictions=predictions,
    )


def _validate_inputs(
    input_path: Path,
    labels_path: Path,
    top_k: int,
) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(f"NIfTI input not found: {input_path}")

    if not (
        input_path.name.endswith(".nii")
        or input_path.name.endswith(".nii.gz")
    ):
        raise ValueError(
            f"Merlin input must be a NIfTI file: {input_path}"
        )

    if not labels_path.is_file():
        raise FileNotFoundError(
            f"Merlin phenotype labels not found: {labels_path}"
        )

    if top_k < 1:
        raise ValueError("top_k must be at least 1")


def _load_phenotype_labels(
    labels_path: Path,
) -> tuple[tuple[str, str], ...]:
    with labels_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as label_file:
        reader = csv.DictReader(label_file)

        expected_columns = {"phecode", "phecode_str"}
        actual_columns = set(reader.fieldnames or ())

        if not expected_columns.issubset(actual_columns):
            raise ValueError(
                "Merlin phenotype labels must contain the columns "
                "'phecode' and 'phecode_str'"
            )

        labels = tuple(
            (
                row["phecode"].strip(),
                row["phecode_str"].strip(),
            )
            for row in reader
        )

    if not labels:
        raise ValueError("Merlin phenotype labels file is empty")

    return labels


def _resolve_device(
    torch: Any,
    requested: DevicePreference,
) -> Literal["cpu", "cuda", "mps"]:
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available")
        return "cuda"

    if requested == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS was requested but is not available")
        return "mps"

    if requested == "cpu":
        return "cpu"

    if torch.backends.mps.is_available():
        return "mps"

    if torch.cuda.is_available():
        return "cuda"

    return "cpu"


def _run_inference(
    torch: Any,
    model: Any,
    image: Any,
    device: Literal["cpu", "cuda", "mps"],
) -> list[float]:
    model = model.to(device)
    image = image.to(device)

    with torch.inference_mode():
        output = model(image)

    if isinstance(output, (tuple, list)):
        output = output[0]

    values = output.squeeze().detach().float().cpu()

    if values.ndim != 1:
        raise RuntimeError(
            "Merlin phenotype output must be one-dimensional after "
            f"removing the batch dimension, got shape {tuple(values.shape)}"
        )

    probabilities = [float(value) for value in values.tolist()]

    if any(value < 0.0 or value > 1.0 for value in probabilities):
        raise RuntimeError(
            "Merlin phenotype output contains values outside [0, 1]"
        )

    return probabilities
