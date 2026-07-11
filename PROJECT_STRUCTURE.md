# Knowledge Extractor Multi Agents Project Structure

## Overview
This project is an AI Agent driven article research and writing workflow. It ingests article metadata from different providers, fetches and cleans article content, extracts topics, generates a draft, reviews it, and publishes the result.

The new blueprint uses `src/` as the root package. The old `agents/` and top-level logic still exist temporarily but have been migrated into `src/`.

## What the project does
- Ingests story metadata from content sources such as Hacker News, Reddit, or RSS
- Fetches and cleans article HTML into text
- Converts cleaned text into a topic prompt for writing
- Generates a draft post using a language model
- Reviews the draft
- Publishes the final result and saves it to JSON

## Folder structure and purpose

### `src/`
This is the new main application package. Everything that should be part of the app lives here.

- `src/ingestion/`
  - Contains providers and ingestion abstractions.
  - `article_provider.py`: the base provider interface (`ArticleProvider`).
  - `provider_registry.py`: registry for provider implementations.
  - `hackernews/`: Hacker News provider implementation.
  - `reddit/`: Reddit provider implementation stub.
  - `rss/`: RSS provider implementation stub.

- `src/processing/`
  - Contains standalone processing nodes.
  - `fetcher/`: fetches and cleans article HTML.
  - `cleaner/`: normalizes raw article payloads.
  - `extractor/`: builds a prompt/text extraction from cleaned article content.
  - `embeddings/`: placeholder embeddings generation.

- `src/repository/`
  - Contains storage abstractions.
  - `article_repository.py`: simple file-based article storage.

- `src/workflow/`
  - Contains workflow nodes and orchestration wrappers.
  - `topic_generation/`: topic analysis and generation.
  - `writing/`: writing node that calls the language model.
  - `reviewing/`: review node.
  - `publishing/`: publish node.
  - `post_writer.py`: migrated LLM post creation logic.

- `src/shared/`
  - Shared utilities.
  - `save.py`: JSON and database save helpers.

### `graphs/`
Contains the workflow graph definition.

- `graphs/nodes.py`: the workflow node functions.
- `graphs/workflow.py`: node registration and transition graph.

### `tests/`
Contains unit tests.

### `agents/` (legacy compatibility)
This contains legacy modules that now forward to `src/` implementations.
They are kept temporarily to avoid breaking any existing references while the migration completes.

### `output/`
- Contains artifacts such as saved workflow JSON and database persistence.

## Why `__init__.py` files exist
In Python, a directory becomes a package when it contains `__init__.py`.
That is similar to declaring a namespace for a folder.
Even when the file is empty, it signals Python that imports from the folder should work.

Example:
- `src/processing/cleaner/__init__.py` lets us import `processing.cleaner.cleaner`
- `src/ingestion/__init__.py` lets us import `ingestion.article_provider`

Without these files, some import systems or older Python versions may not recognize the folders as packages.

## Current use cases

### Add a new source
1. Implement a new provider in `src/ingestion/<source>/`.
2. Register it in `graphs/nodes.py` via `registry.register("<name>", <ProviderClass>)`.
3. Pass the provider name in the workflow state, e.g. `{"provider": "reddit"}`.

### Add a new processing step
1. Add a new class under `src/processing/`.
2. Use it in `graphs/nodes.py` or a workflow node.
3. Test it independently in `tests/`.

### Manage workflow
- `graphs/workflow.py` defines the node order and conditional transitions.
- `graphs/nodes.py` defines the actual business logic for each step.
