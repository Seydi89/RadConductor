from pathlib import Path

import SimpleITK as sitk
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from radconductor.domain.models import (
    DicomSeriesMetadata,
    SegmentationResult,
    VolumeMetadata,
)


class PipelineContext(BaseModel):
    """Mutable state produced during one RadConductor pipeline run."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        validate_assignment=True,
    )

    study_path: Path
    output_directory: Path
    organs: tuple[str, ...] = ("liver", "spleen")

    discovered_series: tuple[DicomSeriesMetadata, ...] = ()
    selected_series: DicomSeriesMetadata | None = None

    image: sitk.Image | None = None
    volume_metadata: VolumeMetadata | None = None

    nifti_path: Path | None = None
    segmentation_result: SegmentationResult | None = None

    qc_passed_organs: set[str] = Field(default_factory=set)
    organ_volumes_ml: dict[str, float] = Field(default_factory=dict)

    @field_validator("organs")
    @classmethod
    def validate_organs(
        cls,
        organs: tuple[str, ...],
    ) -> tuple[str, ...]:
        normalized = tuple(
            organ.strip().lower()
            for organ in organs
            if organ.strip()
        )

        if not normalized:
            raise ValueError("At least one organ must be requested")

        if len(normalized) != len(set(normalized)):
            raise ValueError("Requested organs must be unique")

        return normalized