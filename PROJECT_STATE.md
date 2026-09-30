# Project State

## Current Milestone

Initial multi-model analysis and reporting foundation complete.

## Current Pipeline

```text
DICOM Study
→ Discover Series
→ Select CT Series
→ Load Volume
→ Inspect Volume
→ Save NIfTI
   ├─→ Segment Selected Organs
   │   → Technical Mask QC
   │   → Volume Measurement
   │   → Segmentation Overlays
   │
   └─→ Optional Whole-Scan Merlin Classification
→ HTML Report
```

The segmentation and Merlin branches analyze the same NIfTI scan independently. Merlin does not currently use the selected organs, segmentation masks, QC results, or measurements.

## Current Capabilities

- End-to-end DICOM pipeline
- CT-series discovery and selection
- DICOM-to-NIfTI conversion
- Selected-organ segmentation with TotalSegmentator
- Technical mask validation
- Organ-volume measurement
- Segmentation overlay generation
- Optional Merlin phenotype classification
- Apple Silicon MPS support for Merlin
- Minimal HTML analysis report
- Command-line interface

## Verified Runs

The imaging pipeline and Merlin classification completed successfully on:

```text
data/ct2/Seri3
```

Verified outputs included:

- CT volume metadata
- Liver, spleen, and kidney segmentation and measurement
- Mask overlay PNGs
- Merlin phenotype predictions using MPS

The HTML report implementation compiles. Its final end-to-end output should be confirmed if it has not yet been run after integration.

## Open Problems

- Merlin analyzes the complete CT independently. Selected organs, segmentation masks, QC results, and measurements do not influence its phenotype predictions. A meaningful relationship between the deterministic imaging pipeline and Merlin remains to be designed.

- Mask QC currently verifies technical properties such as mask existence, alignment, and non-empty content. It does not assess anatomical or clinical plausibility, so an implausible organ volume may still pass QC.

- TotalSegmentator produced an incomplete kidney mask while using `--fast` with `--roi_subset`. The mask passed technical QC but yielded an unreliable volume. Future work should compare full-resolution inference, `--robust_crop`, and device configuration before treating measurements as trustworthy.

## Current Architecture

```text
CLI
→ Pipeline
→ Tools and Models
→ Visualization and Reporting
```

`PipelineContext` stores mutable state during execution, including runtime imaging objects and generated result paths.

## Next Task

The next feature has not yet been selected.

Segmentation-quality improvements, anatomical plausibility checks, durable pipeline results, and automated tests remain deferred while core capabilities are developed.
