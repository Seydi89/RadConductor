# RadConductor

RadConductor is currently an open-source, local first medical imaging pipeline with deterministic analysis tools and an Merlin model integration. It aims to evolve into a transparent multi-model framework where medical imaging models, tools, and LLM agents work together.

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
