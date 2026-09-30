# Roadmap

## Vision

RadConductor aims to become a transparent, local-first orchestration framework where medical-imaging models, deterministic tools, and LLM agents collaborate in evidence-grounded workflows.

## Completed

### Imaging Foundation

- DICOM-series discovery
- CT-series selection
- DICOM loading and volume inspection
- NIfTI conversion
- TotalSegmentator integration
- Technical mask QC
- Organ-volume measurement

### Pipeline Foundation

- Dedicated `Pipeline` orchestration layer
- Mutable `PipelineContext`
- Thin command-line interface
- End-to-end DICOM workflow

### Initial Multi-Model Workflow

- Optional Merlin phenotype classification
- CPU, CUDA, and Apple MPS device selection for Merlin
- Pipeline-integrated Merlin execution
- Research-only result labeling

### Visualization and Reporting

- Per-organ segmentation overlay images
- Minimal HTML analysis report
- Technical-QC and non-diagnostic notices

## Near-Term Direction

Select the next meaningful user-facing capability before expanding infrastructure.

Potential work areas include:

- additional deterministic measurements or imaging analysis
- improved visual review and reporting
- additional model integrations
- clearer coordination between model outputs and deterministic tools

## Planned

- Multi-model and LLM-agent orchestration
- Extensible workflows, tools, and reporting

## Deferred Engineering Work

- Anatomical and clinical plausibility checks
- Segmentation-quality modes and device configuration
- Durable serializable pipeline results
- Automated tests and broader safety checks
- Plugin and tool-discovery infrastructure

These items should be revisited as the project gains more capabilities and its intended workflows become clearer.
