import matplotlib.pyplot as plt
import SimpleITK as sitk


def show_middle_slice(image: sitk.Image) -> None:
    """
    Display the middle axial slice of a 3D medical image.
    """

    volume = sitk.GetArrayFromImage(image)

    middle_index = volume.shape[0] // 2
    middle_slice = volume[middle_index]

    plt.figure(figsize=(8, 8))
    plt.imshow(middle_slice, cmap="gray")
    plt.title(f"Axial Slice {middle_index}")
    plt.axis("off")
    plt.show()