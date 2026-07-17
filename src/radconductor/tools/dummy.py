import SimpleITK as sitk

mask = sitk.ReadImage("outputs/segmentations/spleen.nii.gz")
array = sitk.GetArrayFromImage(mask)

print("Size:", mask.GetSize())
print("Spacing:", mask.GetSpacing())
print("Unique values:", set(array.flatten()))
print("Foreground voxels:", (array > 0).sum())