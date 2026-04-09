# Project Overview

## Goal

The repository provides infrastructure for extracting structured mathematical and research-process information from source-side daily notes and using that structured atom layer for downstream retrieval and search.

## Repository Function

The repository defines and operates the structured layer built on top of source notes. It stores schemas, extraction logic, derived atom data, validation and indexing logic, and retrieval/search support.

## Source Model

Daily research notes are the primary human-authored source material for the system. The current authoring workflow uses LaTeX daily-note templates, while canonical structured data lives separately as derived atoms.

## Derived-Layer Principle

The structured layer is derived from source notes. Derived atoms should remain inspectable and be reproducible from the raw source. The structured layer should not become an independent hand-maintained source of truth.

## Main workflow

1. A human writes a daily source note.
2. Codex reads the source note.
3. Codex extracts structured atoms from it.
4. Each atom is saved in a predefined schema-valid format.
5. Validation and indexing scripts process the extracted atoms.
6. Search and retrieval operate over the structured atom layer.

## Atom Families

Atoms are organized into three families:

- `concept`
  - `definition`
  - `notation`
  - `context`
- `statement`
  - `proposition`
  - `conjecture`
  - `observation`
  - `question`
  - `insight`
- `process`
  - `computation`
  - `attempt`
  - `failed_attempt`
  - `proof_idea`
  - `example`
  - `reference_note`

This pass fully specifies `concept.definition` and the `statement` family. The remaining atom types are recognized by the ontology but still need their own dedicated schemas and extraction contracts.

## Shared Atom Requirements

Every atom should include, at minimum:

- stable `atom_id`
- `family`
- type
- atom-specific semantic fields required by its subtype schema

## Storage Strategy

Whenever practical, derived data should be stored as one structured file per atom.

For `concept.definition`, the v1 canonical shape is intentionally minimal:

- `atom_id`
- `family`
- `type`
- `name`
- `body`
- `based_on`
- `axiomatic`
- `aliases`

For `statement`, the shared v1 canonical shape is:

- `atom_id`
- `family`
- `type`
- `body`
- `depends_on`
- `supports`
- `related_to`
- `answered_by`
- `resolved_by`
- `refuted_by`
- `resolution_status`
- `references`

## Retrieval Boundary

Retrieval and search should operate on the structured extracted layer, not on ad hoc parsing of source-note prose.
