import SimpleITK as sitk

from radconductor.domain.models import VolumeMetadata


def inspect_volume(image: sitk.Image) -> VolumeMetadata:
    """Extract basic properties from a loaded 3D medical image."""

    size = image.GetSize()
    spacing = image.GetSpacing()

    range_filter = sitk.MinimumMaximumImageFilter()
    range_filter.Execute(image)

    return VolumeMetadata(
        size=tuple(int(value) for value in size),
        spacing_mm=tuple(float(value) for value in spacing),
        physical_size_mm=tuple(
            float(count * distance)
            for count, distance in zip(size, spacing)
        ),
        voxel_type=image.GetPixelIDTypeAsString(),
        intensity_min=float(range_filter.GetMinimum()),
        intensity_max=float(range_filter.GetMaximum()),
    )