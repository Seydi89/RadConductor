from collections import defaultdict
from pathlib import Path

import pydicom
from pydicom.errors import InvalidDicomError

from radconductor.domain.errors import InvalidStudyError
from radconductor.domain.models import DicomSeriesMetadata


def discover_dicom_series(
    study_root: Path,
) -> list[DicomSeriesMetadata]:
    if not study_root.exists():
        raise InvalidStudyError(
            f"Study root does not exist: {study_root}"
        )

    if not study_root.is_dir():
        raise InvalidStudyError(
            f"Study root must be a directory: {study_root}"
        )

    series_groups: dict[str, list[tuple[Path, object]]] = defaultdict(list)

    for file_path in study_root.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            dataset = pydicom.dcmread(
                file_path,
                stop_before_pixels=True,
                force=False,
            )
        except (InvalidDicomError, OSError):
            continue

        series_uid = getattr(dataset, "SeriesInstanceUID", None)

        if series_uid is None:
            continue

        series_groups[str(series_uid)].append((file_path, dataset))
        
    if not series_groups:
        raise InvalidStudyError(
            "No DICOM series were found in the given study folder."
        )    

    return [
        DicomSeriesMetadata(
            study_root=study_root,
            series_instance_uid=series_uid,
            modality=str(
                getattr(datasets[0][1], "Modality", "UNKNOWN")
            ),
            slice_count=len(datasets),
            files=tuple(sorted(file_path for file_path, _ in datasets)),
        )
        for series_uid, datasets in series_groups.items()
    ]