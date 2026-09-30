# RadConductor

RadConductor is currently an open-source, local-first medical-imaging pipeline for DICOM processing, organ segmentation, technical QC, quantitative measurement, visualization, and optional research AI analysis. It aims to evolve into a transparent orchestration framework where medical-imaging models, deterministic tools, and LLM agents collaborate in evidence-grounded workflows.

## Implemented

- [x] DICOM series discovery and CT-series selection
- [x] DICOM loading and NIfTI conversion
- [x] Organ segmentation with TotalSegmentator
- [x] Technical mask QC
- [x] Organ-volume measurement
- [x] Segmentation overlay images
- [x] Optional whole-scan Merlin phenotype classification
- [x] Minimal HTML analysis report
- [x] Command-line interface

## Not yet implemented

- [ ] Multi-model and LLM-agent orchestration
- [ ] Extensible workflows, tools, and reporting

## Third-party components

RadConductor integrates with, but does not redistribute, the following
third-party model packages and checkpoints:

- TotalSegmentator — Apache License 2.0
- Merlin (`merlin-vlm`) — MIT License

Model weights are downloaded and managed by their upstream packages.
RadConductor outputs are intended for research use only and are not
diagnostic findings.