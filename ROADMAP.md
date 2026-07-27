# Roadmap - Epics and Tasks

## V1

### Done

- DICOM discovery
- CT series selection
- Volume loading
- Inspection
- NIfTI export
- TotalSegmentator integration
- Basic mask QC
- Organ volume measurement
- Initial pipeline orchestration

### Next

- Serializable `PipelineResult`
- Pipeline tests and error handling
- Structured reporting
- Additional deterministic measurements
- CLI cleanup

## Later

- General radiology model runner
- Typed results for different analysis tasks
- Model and tool contracts
- Model registry and plugin system
- Agent-planned pipelines
- Task-specific QC and assurance
- Provenance and evidence bundles
- Model commissioning and monitoring

---

# RadConductor Roadmap

## Vision

RadConductor aims to become a local-first, agentic orchestration platform for radiology AI.

Rather than implementing new AI models, it should provide a clean and modular layer that connects existing imaging tools and models into reproducible analysis workflows. A user or application provides an analysis objective and one or more scans; RadConductor inspects the available data, determines which tools are compatible, constructs an appropriate pipeline, executes it, validates the outputs, and returns traceable results.

RadConductor is not intended to be limited to segmentation. Segmentation is the first implemented model family and the proving ground for the execution architecture. Long term, the platform should support heterogeneous analysis types, including:

- segmentation
- detection
- classification
- quantitative measurement
- vision-language analysis
- embeddings and retrieval
- clinical or outcome prediction
- registration and image transformation
- report generation

Models such as TotalSegmentator, Merlin, MONAI or nnU-Net-based models, and future specialist or foundation models should be integrated behind consistent tool interfaces.

The long-term workflow is:

```text
Analysis objective + imaging data
→ inspect data and acquisition characteristics
→ identify suitable analysis tasks
→ select compatible models and tools
→ construct and validate an execution plan
→ execute the pipeline
→ normalize heterogeneous outputs into typed results
→ apply task-specific QC and assurance
→ return evidence-linked results and reports
```

The agent plans and coordinates the workflow, but does not directly manipulate imaging libraries or invoke models without constraints. Tools perform the analysis, declared contracts define their valid inputs and outputs, and the deterministic execution layer validates and records what was run.

## Scope of V1

The first release remains intentionally narrow:

```text
DICOM discovery
→ CT series selection
→ volume loading
→ NIfTI export
→ TotalSegmentator
→ mask QC
→ organ measurements
→ structured report
```

V1 establishes dependable execution, durable results, error handling, provenance, testing, and reporting. It does not need dynamic agent planning or broad model support.

The architecture should keep the larger direction open without introducing premature abstractions into the current implementation.

---

# Development Roadmap

## Phase 1 — Imaging Foundation

**Status: complete**

Build the deterministic medical-imaging foundation required by later workflows.

Delivered:

- DICOM discovery
- CT series selection
- volume loading
- inspection
- NIfTI export
- TotalSegmentator integration
- basic mask quality control
- organ volume measurement

Outcome:

A working backend that can process a CT study from raw DICOM data to validated organ-volume measurements.

---

## Phase 2 — V1 Pipeline and Durable Results

**Status: in progress**

Move from individually invoked tools to a dependable application workflow while keeping processing logic inside focused tools.

The initial orchestration layer is already in place. The next priority is to separate mutable runtime state from stable application output.

Goals:

- serializable `PipelineResult`
- structured, library-independent result models
- clear error propagation
- execution metadata and output paths
- pipeline-level tests
- a thin CLI that only handles user interaction

Outcome:

A reproducible pipeline that produces a durable result suitable for serialization, reporting, and later orchestration.

---

## Phase 3 — V1 Reporting and Measurements

Transform pipeline results into useful, evidence-linked outputs.

Goals:

- structured JSON output
- human-readable Markdown or HTML reports
- additional deterministic measurements
- quality-control summaries
- input, model, configuration, and execution provenance
- links to generated masks and supporting artifacts

PDF and standardized medical-imaging outputs can follow when the underlying result model is stable.

Outcome:

A complete basic release that turns a CT study into measurements and a reproducible report.

---

## Phase 4 — General Radiology Model Runner

Generalize RadConductor from one fixed segmentation workflow into a runner for heterogeneous radiology AI models and analysis tools.

Goals:

- model and tool capability contracts
- declared input requirements and limitations
- a registry of available models and tools
- typed results for different task families
- reusable adapters around external models
- configurable workflows that do not require CLI changes
- integration of a non-segmentation model, such as Merlin, as the first proof of broader scope

Example result families:

| Analysis type | Result |
|---|---|
| Segmentation | Masks and anatomical structures |
| Detection | Locations, regions, or bounding boxes |
| Classification | Findings, labels, and probabilities |
| Quantification | Volumes, diameters, densities, or burden |
| Vision-language analysis | Findings, descriptions, or report drafts |
| Embeddings and retrieval | Scan representations and similar cases |
| Prediction | Risk or outcome estimates |
| Image transformation | Registered, enhanced, or synthetic images |

Outcome:

A model-agnostic execution layer that can run different radiology analyses and normalize their outputs without treating every model as a segmentation tool.

---

## Phase 5 — Agentic Planning and Orchestration

Allow an agent to translate an analysis objective into a valid and reproducible execution plan.

Goals:

- interpret the requested analysis objective
- inspect modality, anatomy, acquisition, and available series
- identify relevant analysis tasks
- select compatible models and supporting tools
- compose a pipeline from declared capabilities
- validate the plan against tool contracts and policies
- execute, observe, and recover from supported failures
- combine compatible results and identify conflicts
- explain what was run and why

The agent should choose only among registered capabilities. Deterministic code remains responsible for validating inputs, enforcing dependencies, executing tools, and recording provenance.

Outcome:

A controlled agentic system that can construct task-specific radiology workflows without sacrificing reproducibility or auditability.

---

## Phase 6 — Assurance and Evidence

Make quality assessment specific to the analysis task and intended use.

Goals:

- technical input and conversion QC
- task-specific output validation
- anatomical and measurement plausibility checks
- uncertainty, stability, or model-agreement evidence where appropriate
- explicit result states such as accepted, warning, review required, withheld, or inconclusive
- evidence bundles linking each result to its inputs, model, configuration, QC, and limitations
- detection and explanation of conflicting model outputs

The same model output may be adequate for one purpose and inadequate for another. Assurance should therefore apply to typed results and intended uses, not only to segmentation masks.

Outcome:

RadConductor produces not just model outputs, but structured evidence about whether those outputs are suitable for use.

---

## Phase 7 — Extensibility and Model Lifecycle

Turn RadConductor into an extensible platform and quality-control layer for radiology AI over time.

Goals:

- plugin interfaces for models, tools, measurements, QC methods, and report templates
- local model commissioning and qualification profiles
- comparison and revalidation of model versions
- scanner, protocol, and population-shift monitoring
- reviewer feedback and correction capture
- performance surveillance using reviewed cases
- interoperable outputs such as DICOM SEG or Structured Reporting where appropriate

Outcome:

A platform that can add new capabilities without modifying the core workflow engine and can track whether integrated models remain reliable in their operating environment.

---

# Research Direction

The engineering roadmap is broader than any single thesis. A master’s thesis should investigate one bounded scientific claim using RadConductor as its experimental infrastructure.

The current leading direction is:

> Measurement-aware assurance for black-box medical-imaging models: determine when an AI-derived quantitative result can be accepted automatically and when it should be flagged or withheld, including under distribution shift.

A stronger but higher-risk extension is:

> Active counterfactual stress testing: automatically search for clinically plausible scan conditions that cause serious downstream measurement errors, then use the discovered failures to improve runtime assurance.

These ideas should initially be evaluated on one modality, a small number of organs or tasks, frozen external models, and clearly defined downstream errors. They should not expand the scope of V1.

---

# Guiding Principles

Every architectural decision should favor:

- simplicity
- modularity
- typed and explicit interfaces
- deterministic execution
- reproducibility
- traceability
- explainability
- local-first operation
- model and vendor independence
- task-specific quality assurance
- production-quality software engineering
- constrained and auditable agent behavior
