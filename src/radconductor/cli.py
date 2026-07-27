# src/radconductor/cli.py

from pathlib import Path

import typer

from radconductor.pipeline.pipeline import Pipeline

app = typer.Typer(
    help="Local medical-imaging analysis pipeline.",
)


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
) -> None:
    """Run the RadConductor pipeline on a DICOM study."""

    requested_organs = tuple(organs or ["liver", "spleen"])

    pipeline = Pipeline()

    try:
        context = pipeline.run(
            study_path=study_path,
            output_directory=output_directory,
            organs=requested_organs,
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


def main() -> None:
    app()


if __name__ == "__main__":
    main()