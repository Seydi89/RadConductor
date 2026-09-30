# Chat Context and Session Workflow

This document defines how to transfer RadConductor development between chat sessions.

## Sources of Truth

The repository and the following documents are authoritative:

- `PROJECT_STATE.md` — current implemented state and immediate next task
- `ARCHITECTURE.md` — architectural boundaries and dependency direction
- `ENGINEERING_GUIDELINES.md` — development rules
- `ROADMAP.md` — milestones and longer-term priorities
- `HANDOFF.md` — summary of the most recent development session

`CHAT_CONTEXT.md` is generated from these sources. Do not edit it manually.

## Starting a New Chat

Before starting a new chat:

1. Make sure the repository contains the latest completed changes.
2. Make sure `HANDOFF.md` describes the previous session.
3. Generate a fresh context file:

   ```bash
   bash scripts/chat_context_generator.sh
   ```

4. Share `CHAT_CONTEXT.md`.
5. Share the source files directly involved in the next feature.

`CHAT_CONTEXT.md` provides project context, but it does not contain the source-code contents.

## What to Share for a Feature

Always share:

- `CHAT_CONTEXT.md`

Also share the smallest relevant implementation set:

- the file or files expected to change
- directly related domain models or interfaces
- related tests
- relevant configuration
- error messages or example output, when debugging

Examples:

| Task | Additional files to share |
|---|---|
| Pipeline change | Pipeline, context/result models, pipeline tests |
| Tool change | Tool implementation, related domain models, tool tests |
| CLI change | CLI, called application interface, CLI tests |
| Reporting change | Result models, report implementation, report tests |
| Architecture planning | `ROADMAP.md` and relevant design documents |
| Dependency or packaging change | `pyproject.toml` |

Do not share:

- `.env` files or credentials
- patient-identifiable data
- DICOM studies
- model weights
- generated outputs
- virtual environments
- caches such as `__pycache__`
- editor and operating-system files

## Development Process

For each feature:

1. Discuss the design before implementation.
2. Identify the exact files that need to change.
3. Work one file or one coherent change at a time.
4. Explain what changed and why.
5. Run the smallest relevant validation.
6. Confirm the result before continuing.
7. Run broader tests when the feature is complete.

Avoid combining unrelated cleanup with feature work.

## Finishing a Session

At the end of every session:

1. Record what changed in `HANDOFF.md`.
2. Record what was verified.
3. Record known limitations or unfinished work.
4. State the exact next task.

Update other documents only when applicable:

| File | When to update |
|---|---|
| `PROJECT_STATE.md` | After completing a milestone or changing the implemented state |
| `ARCHITECTURE.md` | When architectural boundaries or dependency flow change |
| `ENGINEERING_GUIDELINES.md` | When development standards change |
| `ROADMAP.md` | When priorities, scope, or milestone status change |
| `README.md` | When installation, usage, or user-visible behavior changes |
| `pyproject.toml` | When dependencies, packaging, or commands change |

After updating the relevant documents, regenerate:

```bash
bash scripts/chat_context_generator.sh
```

The regenerated `CHAT_CONTEXT.md` should be the final session artifact used to start the next chat.

## Update and Sharing Summary

| File | Update | Share |
|---|---|---|
| `CHAT_CONTEXT.md` | Regenerate at the end of a session | Every new chat |
| `HANDOFF.md` | End of every session | Included through `CHAT_CONTEXT.md` |
| `PROJECT_STATE.md` | After implemented state changes | Included through `CHAT_CONTEXT.md` |
| `ARCHITECTURE.md` | Only after architecture changes | Included through `CHAT_CONTEXT.md` |
| `ENGINEERING_GUIDELINES.md` | Only after standards change | Included through `CHAT_CONTEXT.md` |
| `ROADMAP.md` | After priority or scope changes | Planning discussions |
| Feature source files | During feature implementation | When working on that feature |
| Related tests | With the corresponding implementation | When implementing or debugging |
