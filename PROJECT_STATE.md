# Project State

## Current Milestone

Phase 2 pipeline orchestration foundation complete.

## Current Pipeline

DICOM
→ Discover
→ Select
→ Load
→ Inspect
→ Save NIfTI
→ Segment
→ QC
→ Measure

## Current Status

* End-to-end DICOM pipeline works.
* TotalSegmentator integration works.
* Basic mask QC works.
* Organ volume measurement works.
* Pipeline orchestration moved out of the CLI.
* Runtime state is stored in `PipelineContext`.
* CLI now calls the pipeline as its application entry point.

## Current Architecture

```text
CLI
→ Pipeline
→ Tools
→ Domain Models
```

## Next Task

Add a serializable `PipelineResult` separate from `PipelineContext`.

After that:

1. reporting
2. additional measurements
3. AI/LLM integration
4. plugin and tool system
