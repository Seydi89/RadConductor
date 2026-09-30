# RadConductor Session Handoff

## Session Summary

This session expanded RadConductor from a deterministic organ-analysis pipeline into an initial multi-model workflow with visual QC and reporting.

The project now supports:

- DICOM discovery, CT selection, loading, and NIfTI conversion
- TotalSegmentator organ segmentation
- Technical mask QC and organ-volume measurement
- Segmentation overlay images
- Optional whole-scan Merlin phenotype classification
- Minimal HTML report generation

## Current Flow

```text
DICOM Study
→ Discover and Select CT Series
→ Load and Inspect Volume
→ Save NIfTI
   ├─→ TotalSegmentator
   │   → Technical Mask QC
   │   → Volume Measurement
   │   → Mask Overlay PNGs
   │
   └─→ Optional Merlin Phenotype Classification
→ HTML Report
```

Merlin and organ segmentation are independent analyses of the same NIfTI volume. Organ selection does not affect Merlin predictions.

## Work Completed

### Merlin Integration

Added typed domain models for Merlin phenotype predictions and results.

Added:

```text
src/radconductor/tools/classification/run_merlin.py
```

The runner:

- lazily imports Merlin and PyTorch
- validates NIfTI input and phenotype labels
- supports `auto`, `cpu`, `cuda`, and `mps`
- falls back from MPS to CPU for supported runtime failures
- returns the highest-probability phenotypes as typed domain data

Added the standalone command:

```text
radconductor merlin-phenotypes
```

Merlin was also integrated as an optional final analysis stage of the main `inspect` workflow through `--run-merlin`.

### Pipeline Integration

`PipelineContext` now stores:

- optional Merlin results
- mask overlay paths
- the generated HTML report path

`Pipeline` now:

- optionally runs Merlin on the complete generated NIfTI volume
- creates segmentation overlays after mask validation and measurement
- writes a minimal HTML report after all requested analysis stages

### Segmentation Visualization

Added:

```text
src/radconductor/tools/viz/create_mask_overlay.py
```

For every selected organ, the tool:

- finds the axial slice with the largest mask area
- renders the CT using a soft-tissue window
- adds a colored mask overlay and outline
- includes the measured volume in the title
- saves a headless PNG for technical review

The overlays exposed an incomplete right-kidney segmentation that had passed the existing technical QC checks.

### Reporting

Added:

```text
src/radconductor/reporting/html_report.py
```

The minimal report includes:

- scan and selected-series information
- organ measurements and technical QC status
- segmentation overlay images
- optional Merlin phenotype predictions
- research-only and non-diagnostic notices

The report is written to:

```text
<output-directory>/report.html
```

### Documentation and Licensing

The README now distinguishes current capabilities from the intended future direction.

Added Merlin attribution for the redistributed phenotype label mapping:

```text
resources/merlin/NOTICE.md
```

Merlin remains an optional dependency. Merlin and TotalSegmentator model checkpoints are downloaded by their upstream packages and are not stored in the repository.

## Verified Results

Standalone and pipeline-integrated Merlin inference completed successfully on Apple Silicon using MPS.

Example top predictions for the tested CT included:

- Abdominal pain
- Other tests
- Nausea and vomiting
- Injury, NOS
- Back pain

The combined pipeline completed successfully on:

```text
data/ct2/Seri3
```

Segmentation overlays were generated and opened successfully.

The HTML report code compiles. If a final pipeline run was not performed after report integration, confirm `report.html` generation at the beginning of the next session.

## Known Limitations

- Merlin performs whole-scan phenotype classification independently of organ segmentation and measurement.
- Technical mask QC does not establish anatomical or clinical plausibility.
- TotalSegmentator produced an incomplete kidney mask while using `--fast` with `--roi_subset`.
- TotalSegmentator was resolved from a global Homebrew installation and ran on CPU during the observed run.
- No automated tests exist yet.
- `PipelineContext` still contains runtime objects and is not a durable serializable result.
- Outputs are research-only and must not be used for diagnosis or clinical decision-making.

## Files Added or Updated

```text
pyproject.toml
README.md
PROJECT_STATE.md
HANDOFF.md
ARCHITECTURE.md
ROADMAP.md
src/radconductor/domain/models.py
src/radconductor/cli.py
src/radconductor/pipeline/context.py
src/radconductor/pipeline/pipeline.py
src/radconductor/tools/classification/run_merlin.py
src/radconductor/tools/viz/create_mask_overlay.py
src/radconductor/reporting/html_report.py
resources/merlin/phenotypes.csv
resources/merlin/NOTICE.md
```

## Next Task

The next feature has not been selected.

Continue one feature and one file at a time. Preserve the deferred issues above without treating them as blockers unless they directly affect the selected feature.
