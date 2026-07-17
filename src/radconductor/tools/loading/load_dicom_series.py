from pathlib import Path

import SimpleITK as sitk

from radconductor.domain.models import DicomSeriesMetadata


def load_dicom_series(
    series: DicomSeriesMetadata,
) -> sitk.Image:
    """Load a DICOM series using geometry-aware DICOM slice ordering."""

    if not series.files:
        raise ValueError(
            f"Series {series.series_instance_uid} contains no files."
        )

    series_directory = series.files[0].parent

    file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
        str(series_directory),
        series.series_instance_uid,
    )

    if not file_names:
        raise ValueError(
            f"Could not obtain ordered files for series "
            f"{series.series_instance_uid} in {series_directory}"
        )

    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(file_names)

    return reader.Execute()