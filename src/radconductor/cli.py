from pathlib import Path

import typer

from radconductor.tools.inspection.discover_dicom_series import (
    discover_dicom_series,
)
from radconductor.tools.inspection.inspect_volume import inspect_volume
from radconductor.tools.loading.load_dicom_series import load_dicom_series
from radconductor.tools.viz.show_slice import show_middle_slice

app = typer.Typer()

@app.callback()
def main() -> None:
    """RadConductor CLI."""

@app.command()
def inspect(study_path: str):
    """Inspect a DICOM study."""

    series = discover_dicom_series(Path(study_path))

    print()

    for i, s in enumerate(series, start=1):
        print(f"Series {i}")
        print(f"UID: {s.series_instance_uid}")
        print(f"Modality: {s.modality}")
        print(f"Slices: {s.slice_count}")
        print()
        
    image = load_dicom_series(series[0])
    # print(f"Dimension: {image.GetDimension()}")
    # print(f"Size: {image.GetSize()}")
    # print(f"Spacing: {image.GetSpacing()}")
    # print(f"Origin: {image.GetOrigin()}")
    # print(f"Direction: {image.GetDirection()}")   
    
    # show_middle_slice(image)
    
    metadata = inspect_volume(image)

    print(f"Size: {metadata.size}")
    print(f"Spacing: {metadata.spacing_mm}")
    print(f"Physical size: {metadata.physical_size_mm}")
    print(f"Voxel type: {metadata.voxel_type}")
    print(
        f"Intensity range: "
        f"{metadata.intensity_min} to {metadata.intensity_max}"
    )


def main():
    app()


if __name__ == "__main__":
    main()