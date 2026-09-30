# Architecture

## Principles

- One responsibility per module.
- CLI handles user interaction only.
- Pipeline coordinates execution only.
- Tools contain individual processing operations.
- Domain models contain stable application data.
- External models and executables are wrapped behind local interfaces.
- `SimpleITK.Image` is the canonical in-memory volume.
- Runtime state and durable results should remain separate.
- Research AI outputs must remain distinguishable from deterministic measurements.
- Avoid premature abstraction.

## Logical Flow

```text
DICOM Study
→ Discover Series
→ Select CT Series
→ Load Volume
→ Inspect Volume
→ Save NIfTI
   ├─→ Organ Segmentation
   │   → Technical Mask QC
   │   → Measurements
   │   → Visual Overlays
   │
   └─→ Optional Whole-Scan Merlin Classification
→ HTML Report
```

The segmentation and Merlin branches share the NIfTI input but are otherwise independent. Merlin does not consume organ masks, QC results, or measurements.

## Dependency Flow

```text
CLI
→ Pipeline
→ Reporting and Tools
→ Domain Models
```

Third-party libraries and executables are accessed only through tool modules.

## CLI

The CLI:

- parses user arguments
- selects optional pipeline capabilities
- invokes `Pipeline`
- displays completed results and output paths
- converts failures into clear command-line errors

The CLI does not perform imaging, segmentation, classification, measurement, or reporting logic.

## Pipeline Context

`PipelineContext` represents mutable state during one pipeline execution.

It may contain:

- input and output paths
- requested organs
- discovered and selected DICOM-series metadata
- a runtime `SimpleITK.Image`
- volume metadata
- segmentation outputs
- technical QC and measurement results
- segmentation overlay paths
- optional Merlin results
- the HTML report path

It is not a durable or fully serializable application result.

## Pipeline

`Pipeline` defines execution order and coordinates existing operations.

It does not implement:

- DICOM parsing
- segmentation algorithms
- mask validation rules
- measurement calculations
- Merlin inference internals
- visualization rendering
- HTML rendering

The current implementation executes Merlin after segmentation when enabled, although the two analyses are logically independent.

## Tools

Each tool has one focused responsibility and may wrap an external library or executable.

Current tool groups include:

- inspection: DICOM discovery and volume inspection
- selection: CT-series selection
- loading: DICOM-series loading
- conversion: NIfTI export
- segmentation: TotalSegmentator execution
- QC: technical mask validation
- measurement: organ-volume calculation
- visualization: CT and mask overlay generation
- classification: Merlin phenotype inference

## Reporting

The reporting layer converts completed pipeline state into user-facing artifacts.

The current HTML report is intentionally minimal. It references generated images through relative paths and includes explicit research-only and technical-QC notices.

Reporting does not interpret measurements or predictions clinically.

## Domain

Domain models represent stable application data and remain independent of imaging libraries and external model implementations.

Current models cover:

- DICOM-series metadata
- volume metadata
- segmentation results
- Merlin phenotype predictions and results

## External Systems

### TotalSegmentator

TotalSegmentator provides selected-organ segmentation. RadConductor invokes its CLI and validates the expected mask outputs.

### Merlin

Merlin provides optional whole-scan phenotype probabilities. RadConductor loads Merlin lazily so the deterministic imaging pipeline remains usable without the optional dependency.

Neither dependency's model checkpoints are stored in the RadConductor repository.

## Current Boundaries

- Technical QC is not anatomical or clinical validation.
- Merlin predictions are not conditioned on selected organs.
- No LLM-agent orchestration exists yet.
- No plugin system exists yet.
- No durable `PipelineResult` exists yet.
