# Architecture

## Principles

- One responsibility per module.
- CLI only orchestrates.
- Domain models are library-independent.
- External tools are wrapped.
- SimpleITK.Image is the canonical volume.

## Flow

CLI
→ Tools
→ Domain