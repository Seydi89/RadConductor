from pathlib import Path

import SimpleITK as sitk


def measure_mask_volume(mask_path: Path) -> float:
    """Return the binary mask volume in millilitres."""

    if not mask_path.exists():
        raise FileNotFoundError(f"Mask not found: {mask_path}")

    mask = sitk.ReadImage(str(mask_path))

    voxel_count = int(
        sitk.GetArrayViewFromImage(mask).astype(bool).sum()
    )

    voxel_volume_mm3 = (
        mask.GetSpacing()[0]
        * mask.GetSpacing()[1]
        * mask.GetSpacing()[2]
    )

    return voxel_count * voxel_volume_mm3 / 1000.0