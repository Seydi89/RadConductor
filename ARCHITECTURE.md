# Architecture

## Principles

* One responsibility per module.
* CLI handles user interaction only.
* Pipeline coordinates execution only.
* Tools contain individual processing operations.
* Domain models are library-independent.
* External tools are wrapped.
* SimpleITK.Image is the canonical in-memory volume.
* Runtime state and durable results should remain separate.
* Avoid premature abstraction.

## Dependency Flow

```text
CLI
→ Pipeline
→ Tools
→ Domain Models
```

## Pipeline Context

`PipelineContext` represents mutable state during one pipeline execution.

It may contain runtime objects such as `SimpleITK.Image` and should not be used directly as a report or serialized application result.

## Pipeline

`Pipeline` defines the execution order and coordinates existing tools.

It does not contain DICOM, segmentation, QC, or measurement logic.

## Tools

Each tool has one focused responsibility and may wrap an external library or executable.

Examples:

* DICOM discovery
* CT series selection
* volume loading
* image inspection
* NIfTI conversion
* segmentation
* mask validation
* measurements

## Domain

Domain models represent stable application data and remain independent of imaging libraries and external tools.
