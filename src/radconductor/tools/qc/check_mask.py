from pathlib import Path

import SimpleITK as sitk


def check_mask(
    mask_path: Path,
    reference_image: sitk.Image,
) -> None:
    """Validate basic consistency of a segmentation mask."""

    if not mask_path.exists():
        raise FileNotFoundError(f"Mask not found: {mask_path}")

    mask = sitk.ReadImage(str(mask_path))

    if mask.GetSize() != reference_image.GetSize():
        raise ValueError(
            f"Mask size {mask.GetSize()} does not match "
            f"CT size {reference_image.GetSize()}."
        )

    if mask.GetSpacing() != reference_image.GetSpacing():
        raise ValueError(
            f"Mask spacing {mask.GetSpacing()} does not match "
            f"CT spacing {reference_image.GetSpacing()}."
        )

    array = sitk.GetArrayViewFromImage(mask)
    unique_values = set(array.ravel())

    if not unique_values.issubset({0, 1}):
        raise ValueError(
            f"Mask is not binary. Found values: {unique_values}"
        )

    foreground_voxels = int((array > 0).sum())

    if foreground_voxels == 0:
        raise ValueError("Mask contains no foreground voxels.")