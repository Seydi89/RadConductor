from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict


# class ImageMetadata(BaseModel):
#     """Basic metadata extracted from a medical image input."""

#     model_config = ConfigDict(frozen=True, extra="forbid")

#     source_path: Path
#     source_format: Literal["nifti", "dicom"]
#     shape: tuple[int, ...]
#     spacing_mm: tuple[float, ...]


class DicomSeriesMetadata(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    study_root: Path
    series_instance_uid: str
    modality: str
    slice_count: int
    files: tuple[Path, ...]
    
    
class VolumeMetadata(BaseModel):
    """Basic properties of a loaded three-dimensional image."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    size: tuple[int, int, int] # voxel count in (x, y, z)
    spacing_mm: tuple[float, float, float] # physical size of each voxel
    physical_size_mm: tuple[float, float, float] # approximate physical coverage of the volume
    voxel_type: str # for example, signed 16-bit integer
    intensity_min: float
    intensity_max: float    