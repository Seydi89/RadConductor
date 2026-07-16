import SimpleITK as sitk

from radconductor.domain.models import DicomSeriesMetadata


def load_dicom_series(
    series: DicomSeriesMetadata,
) -> sitk.Image:
    """Load a discovered DICOM series as a 3D image."""

    if not series.files:
        raise ValueError(
            f"Series {series.series_instance_uid} contains no files."
        )

    file_names = [str(path) for path in series.files]

    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(file_names)

    return reader.Execute()