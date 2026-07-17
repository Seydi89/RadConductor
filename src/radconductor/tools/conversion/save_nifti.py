from pathlib import Path

import SimpleITK as sitk


def save_nifti(
    image: sitk.Image,
    output_path: Path,
) -> Path:
    """Save a 3D medical image as a compressed NIfTI file."""
    
    z_spacing = image.GetSpacing()[2]

    if z_spacing < 0.1:
        raise ValueError(
            f"Implausible slice spacing detected: {z_spacing} mm. "
            "The DICOM slices may be incorrectly ordered."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    sitk.WriteImage(
        image,
        str(output_path),
        useCompression=True,
    )

    return output_path