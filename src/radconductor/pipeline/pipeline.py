from pathlib import Path

from radconductor.pipeline.context import PipelineContext
from radconductor.tools.conversion.save_nifti import save_nifti
from radconductor.tools.inspection.discover_dicom_series import (
    discover_dicom_series,
)
from radconductor.tools.inspection.inspect_volume import inspect_volume
from radconductor.tools.loading.load_dicom_series import load_dicom_series
from radconductor.tools.measurement.measure_mask_volume import (
    measure_mask_volume,
)
from radconductor.tools.qc.check_mask import check_mask
from radconductor.tools.segmentation.segment_organs import segment_organs
from radconductor.tools.selection.select_series import select_ct_series


class Pipeline:
    """Run the deterministic RadConductor imaging pipeline."""

    def run(
        self,
        study_path: Path,
        output_directory: Path,
        organs: tuple[str, ...] = ("liver", "spleen"),
    ) -> PipelineContext:
        context = PipelineContext(
            study_path=study_path,
            output_directory=output_directory,
            organs=organs,
        )

        self._prepare_output_directory(context)
        self._discover_series(context)
        self._select_series(context)
        self._load_volume(context)
        self._inspect_volume(context)
        self._save_nifti(context)
        self._segment_organs(context)
        self._validate_and_measure_masks(context)

        return context

    def _prepare_output_directory(
        self,
        context: PipelineContext,
    ) -> None:
        context.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _discover_series(
        self,        
        context: PipelineContext,
    ) -> None:
        series = discover_dicom_series(context.study_path)

        if not series:
            raise ValueError(
                f"No DICOM series found under {context.study_path}"
            )

        context.discovered_series = tuple(series)

    def _select_series(
        self,        
        context: PipelineContext,
    ) -> None:
        context.selected_series = select_ct_series(
            context.discovered_series
        )

    def _load_volume(
        self,        
        context: PipelineContext,
    ) -> None:
        if context.selected_series is None:
            raise RuntimeError(
                "A DICOM series must be selected before loading"
            )

        context.image = load_dicom_series(
            context.selected_series
        )

    def _inspect_volume(
        self,        
        context: PipelineContext,
    ) -> None:
        if context.image is None:
            raise RuntimeError(
                "A volume must be loaded before inspection"
            )

        context.volume_metadata = inspect_volume(
            context.image
        )

    def _save_nifti(
        self,        
        context: PipelineContext,
    ) -> None:
        if context.image is None:
            raise RuntimeError(
                "A volume must be loaded before NIfTI export"
            )

        nifti_path = (
            context.output_directory
            / "scan.nii.gz"
        )

        context.nifti_path = save_nifti(
            context.image,
            nifti_path,
        )

    def _segment_organs(
        self,        
        context: PipelineContext,
    ) -> None:
        if context.nifti_path is None:
            raise RuntimeError(
                "A NIfTI image must be created before segmentation"
            )

        segmentation_directory = (
            context.output_directory
            / "segmentations"
        )

        context.segmentation_result = segment_organs(
            input_path=context.nifti_path,
            output_directory=segmentation_directory,
            organs=list(context.organs),
        )

    def _validate_and_measure_masks(
        self,        
        context: PipelineContext,
    ) -> None:
        if context.image is None:
            raise RuntimeError(
                "The reference volume is unavailable"
            )

        if context.segmentation_result is None:
            raise RuntimeError(
                "Segmentation must run before mask validation"
            )

        for organ in context.organs:
            try:
                mask_path = context.segmentation_result.masks[organ]
            except KeyError as exc:
                raise RuntimeError(
                    f"Segmentation output is missing the "
                    f"requested organ: {organ}"
                ) from exc

            check_mask(
                mask_path=mask_path,
                reference_image=context.image,
            )

            context.qc_passed_organs.add(organ)
            context.organ_volumes_ml[organ] = (
                measure_mask_volume(mask_path)
            )