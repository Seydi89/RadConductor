from pathlib import Path
import subprocess

from radconductor.domain.models import SegmentationResult


def segment_organs(
    input_path: Path,
    output_directory: Path,
    organs: list[str],
) -> SegmentationResult:
    """Run TotalSegmentator for the requested organs."""

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    output_directory.mkdir(parents=True, exist_ok=True)

    command = [
        "TotalSegmentator",
        "-i",
        str(input_path),
        "-o",
        str(output_directory),
        "--roi_subset",
        *organs,
        "--fast",
    ]

    subprocess.run(
        command,
        check=True,
    )

    masks = {
        organ: output_directory / f"{organ}.nii.gz"
        for organ in organs
    }

    missing_masks = [
        organ
        for organ, mask_path in masks.items()
        if not mask_path.exists()
    ]

    if missing_masks:
        raise RuntimeError(
            f"Segmentation completed, but masks are missing: {missing_masks}"
        )

    return SegmentationResult(
        input_path=input_path,
        output_directory=output_directory,
        masks=masks,
    )