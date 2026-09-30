from enum import Enum
from pathlib import Path

import typer

from radconductor.pipeline.pipeline import Pipeline
from radconductor.tools.classification.run_merlin import (
    run_merlin_phenotype_classification,
)

app = typer.Typer(
    help="Local medical-imaging analysis pipeline.",
)


class MerlinDevice(str, Enum):
    AUTO = "auto"
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"


@app.callback()
def callback() -> None:
    """RadConductor CLI."""


@app.command()
def inspect(
    study_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing the DICOM study.",
    ),
    output_directory: Path = typer.Option(
        Path("outputs"),
        "--output-dir",
        "-o",
        help="Directory where pipeline outputs are written.",
    ),
    organs: list[str] | None = typer.Option(
        None,
        "--organ",
        help=(
            "Organ to segment. Repeat this option to request "
            "multiple organs."
        ),
    ),
    run_merlin: bool = typer.Option(
        False,
        "--run-merlin",
        help="Run research-only Merlin phenotype classification.",
    ),
    merlin_labels_path: Path = typer.Option(
        Path("resources/merlin/phenotypes.csv"),
        "--merlin-labels",
        help="Merlin phenotype label mapping.",
    ),
    merlin_cache_directory: Path | None = typer.Option(
        None,
        "--merlin-cache-dir",
        help=(
            "Directory for Merlin preprocessing. Defaults to "
            "<output-dir>/merlin_cache."
        ),
    ),
    merlin_top_k: int = typer.Option(
        5,
        "--merlin-top-k",
        min=1,
        max=1692,
        help="Number of Merlin phenotype predictions to display.",
    ),
    merlin_device: MerlinDevice = typer.Option(
        MerlinDevice.AUTO,
        "--merlin-device",
        case_sensitive=False,
        help="Merlin inference device: auto, mps, cuda, or cpu.",
    ),
) -> None:
    """Run the RadConductor pipeline on a DICOM study."""

    requested_organs = tuple(organs or ["liver", "spleen"])

    if run_merlin:
        typer.secho(
            "Merlin outputs are for research use only and are not "
            "diagnostic findings.",
            fg=typer.colors.YELLOW,
        )

    pipeline = Pipeline()

    try:
        context = pipeline.run(
            study_path=study_path,
            output_directory=output_directory,
            organs=requested_organs,
            run_merlin=run_merlin,
            merlin_labels_path=merlin_labels_path,
            merlin_cache_directory=merlin_cache_directory,
            merlin_top_k=merlin_top_k,
            merlin_device=merlin_device.value,
        )
    except Exception as exc:
        typer.secho(
            f"Pipeline failed: {exc}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1) from exc

    typer.secho(
        "Pipeline completed successfully.",
        fg=typer.colors.GREEN,
    )

    typer.echo()
    typer.echo(f"Study: {context.study_path}")
    typer.echo(f"Output directory: {context.output_directory}")

    if context.selected_series is not None:
        typer.echo()
        typer.echo("Selected DICOM series")
        typer.echo(
            f"  UID: {context.selected_series.series_instance_uid}"
        )
        typer.echo(
            f"  Modality: {context.selected_series.modality}"
        )
        typer.echo(
            f"  Slices: {context.selected_series.slice_count}"
        )

    if context.volume_metadata is not None:
        metadata = context.volume_metadata

        typer.echo()
        typer.echo("Volume")
        typer.echo(f"  Size: {metadata.size}")
        typer.echo(f"  Spacing: {metadata.spacing_mm} mm")
        typer.echo(
            f"  Physical size: {metadata.physical_size_mm} mm"
        )
        typer.echo(f"  Voxel type: {metadata.voxel_type}")
        typer.echo(
            "  Intensity range: "
            f"{metadata.intensity_min} "
            f"to {metadata.intensity_max}"
        )

    if context.nifti_path is not None:
        typer.echo()
        typer.echo(f"NIfTI: {context.nifti_path}")

    if context.organ_volumes_ml:
        typer.echo()
        typer.echo("Measurements")

        for organ, volume_ml in context.organ_volumes_ml.items():
            qc_status = (
                "QC passed"
                if organ in context.qc_passed_organs
                else "QC unavailable"
            )

            typer.echo(
                f"  {organ}: {volume_ml:.1f} mL — {qc_status}"
            )
            
    if context.mask_overlay_paths:
        typer.echo()
        typer.echo("Segmentation overlays — technical review only")

        for organ, overlay_path in context.mask_overlay_paths.items():
            typer.echo(f"  {organ}: {overlay_path}")        

    if context.merlin_result is not None:
        result = context.merlin_result

        typer.echo()
        typer.echo("Merlin phenotype predictions — research only")
        typer.echo(f"  Device: {result.device}")
        typer.echo(
            f"  Model: {result.model_name} {result.model_version}"
        )

        for rank, prediction in enumerate(
            result.predictions,
            start=1,
        ):
            typer.echo(
                f"  {rank}. {prediction.description} "
                f"[{prediction.phecode}] — "
                f"{prediction.probability:.4f}"
            )
    
    if context.report_path is not None:
        typer.echo()
        typer.echo(f"HTML report: {context.report_path}")        


@app.command("merlin-phenotypes")
def merlin_phenotypes(
    input_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="NIfTI CT volume to analyze with Merlin.",
    ),
    labels_path: Path = typer.Option(
        Path("resources/merlin/phenotypes.csv"),
        "--labels",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Merlin phenotype label mapping.",
    ),
    cache_directory: Path = typer.Option(
        Path("outputs/merlin_cache"),
        "--cache-dir",
        help="Directory used for preprocessed Merlin input data.",
    ),
    top_k: int = typer.Option(
        5,
        "--top-k",
        min=1,
        max=1692,
        help="Number of highest-probability phenotypes to display.",
    ),
    device: MerlinDevice = typer.Option(
        MerlinDevice.AUTO,
        "--device",
        case_sensitive=False,
        help="Inference device: auto, mps, cuda, or cpu.",
    ),
) -> None:
    """Run research-only Merlin phenotype analysis on a NIfTI CT."""

    typer.secho(
        "Research use only — outputs are not diagnostic findings.",
        fg=typer.colors.YELLOW,
    )

    try:
        result = run_merlin_phenotype_classification(
            input_path=input_path,
            labels_path=labels_path,
            cache_directory=cache_directory,
            top_k=top_k,
            device=device.value,
        )
    except Exception as exc:
        typer.secho(
            f"Merlin analysis failed: {exc}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1) from exc

    typer.secho(
        "Merlin analysis completed successfully.",
        fg=typer.colors.GREEN,
    )
    typer.echo(f"Input: {result.input_path}")
    typer.echo(f"Device: {result.device}")
    typer.echo(f"Model: {result.model_name} {result.model_version}")
    typer.echo()
    typer.echo("Top phenotype predictions")

    for rank, prediction in enumerate(result.predictions, start=1):
        typer.echo(
            f"  {rank}. {prediction.description} "
            f"[{prediction.phecode}] — "
            f"{prediction.probability:.4f}"
        )


def main() -> None:
    app()


if __name__ == "__main__":
    main()