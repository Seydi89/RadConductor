from pathlib import Path

import numpy as np
import SimpleITK as sitk
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def create_mask_overlay(
    reference_image: sitk.Image,
    mask_path: Path,
    output_path: Path,
    organ_name: str,
    volume_ml: float | None = None,
) -> Path:
    """Save an axial CT slice with its segmentation mask overlaid.

    The selected slice contains the largest number of foreground mask
    voxels. The image is intended for technical review, not clinical use.
    """

    if not mask_path.is_file():
        raise FileNotFoundError(f"Mask not found: {mask_path}")

    if output_path.suffix.lower() != ".png":
        raise ValueError("Mask overlay output must be a PNG file")

    normalized_organ_name = organ_name.strip()
    if not normalized_organ_name:
        raise ValueError("Organ name must not be empty")

    if volume_ml is not None and volume_ml < 0:
        raise ValueError("Organ volume must not be negative")

    mask_image = sitk.ReadImage(str(mask_path))

    if mask_image.GetSize() != reference_image.GetSize():
        raise ValueError(
            f"Mask size {mask_image.GetSize()} does not match "
            f"CT size {reference_image.GetSize()}"
        )

    ct_array = sitk.GetArrayViewFromImage(reference_image)
    mask_array = sitk.GetArrayFromImage(mask_image) > 0

    slice_areas = mask_array.sum(axis=(1, 2))
    if not np.any(slice_areas):
        raise ValueError("Mask contains no foreground voxels")

    slice_index = int(np.argmax(slice_areas))
    ct_slice = ct_array[slice_index]
    mask_slice = mask_array[slice_index]

    title = (
        f"{normalized_organ_name} segmentation — "
        f"axial slice {slice_index}"
    )
    if volume_ml is not None:
        title += f" — {volume_ml:.1f} mL"

    figure = Figure(figsize=(8, 8), constrained_layout=True)
    FigureCanvasAgg(figure)
    axes = figure.subplots()

    axes.imshow(
        ct_slice,
        cmap="gray",
        vmin=-160,
        vmax=240,
    )
    axes.imshow(
        np.ma.masked_where(~mask_slice, mask_slice),
        cmap="autumn",
        alpha=0.4,
        interpolation="none",
        vmin=0,
        vmax=1,
    )
    axes.contour(
        mask_slice,
        levels=[0.5],
        colors=["red"],
        linewidths=1,
    )
    axes.set_title(title)
    axes.axis("off")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )
    figure.clear()

    return output_path