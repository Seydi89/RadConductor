# Roadmap - Epics/Tasks

## Done

- DICOM discovery
- Volume loading
- Inspection
- NIfTI export
- TotalSegmentator
- QC
- Volume measurement

## Next

- Pipeline
- Reporting
- Measurements
- LLM
- Plugins

# RadConductor Roadmap

# Vision

RadConductor aims to become a local-first orchestration framework for medical imaging workflows.

Rather than implementing new AI models, its goal is to provide a clean, modular layer that connects existing medical imaging tools into a coherent pipeline. The framework should allow users, researchers, and eventually AI agents to perform complex imaging workflows through a simple and consistent interface.

Long-term, RadConductor should be able to:

- discover and organize medical imaging studies
- inspect and validate imaging data
- orchestrate multiple AI models
- perform deterministic measurements
- generate reproducible reports
- expose every capability as reusable tools for an LLM agent

The project emphasizes software architecture, reliability, modularity and extensibility rather than developing new segmentation or deep learning algorithms.


---

# Development Roadmap

## Phase 1 — Imaging Foundation

Build the deterministic medical imaging pipeline.

The objective of this phase is to reliably load medical imaging data, convert it into a canonical internal representation, run AI segmentation models, validate the outputs, and compute reproducible measurements.

Deliverables include:

- DICOM discovery
- CT series selection
- volume loading
- inspection
- NIfTI export
- TotalSegmentator integration
- quality control
- organ measurements

Outcome:

A reliable backend capable of processing a medical study from raw DICOM images to quantitative measurements.


---

## Phase 2 — Pipeline Layer

Move from individual tools to workflow orchestration.

Instead of the CLI manually calling every function, introduce a pipeline that coordinates the complete analysis process while keeping individual tools independent.

Goals:

- pipeline orchestration
- shared execution context
- structured results
- cleaner CLI
- better error propagation
- testing


---

## Phase 3 — Reporting

Transform raw measurements into useful outputs.

The reporting layer should produce human-readable summaries while preserving links to the underlying evidence.

Possible outputs:

- Markdown
- HTML
- PDF
- structured JSON

Reports should combine:

- measurements
- quality-control results
- screenshots
- metadata
- execution logs


---

## Phase 4 — Agent Integration

Expose RadConductor as a toolbox for LLMs.

Instead of directly invoking imaging libraries, an AI agent should interact with high-level RadConductor tools.

Example:

Patient CT

↓

Segment liver

↓

Measure volume

↓

Generate report

↓

Answer clinical question


The agent should never manipulate SimpleITK or TotalSegmentator directly.


---

## Phase 5 — Extensibility

Turn RadConductor into a platform.

Future functionality should be added through well-defined extension points rather than modifying existing code.

Examples:

- additional segmentation models
- registration algorithms
- radiomics
- report templates
- custom measurements
- new AI providers


---

# Guiding Principles

Every architectural decision should favor:

- simplicity
- modularity
- deterministic execution
- reproducibility
- explainability
- local-first execution
- production-quality software engineering