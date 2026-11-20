# CLV — Command Library Vault

Searchable personal library of technical commands and references.

## Requirements
- **Main tabs** (initial examples, not fixed): Python, Linux, Networking, Windows, Cybersecurity — user can add more.
- Each tab has **nested categories**, e.g.:
  ```
  Networking
  ├── Connectivity & Path Testing
  └── Interface
  Python
  ├── File Handling
  ├── Lists
  └── Dictionaries
  ```
- Each command: name, description, parameter explanations, usage examples, personal notes.
- Search across commands (name, description, notes); optionally filter by tab/category.

## Implementation notes
- Tabs and categories are **data, not code** — stored in the DB so new ones need no code changes.
- Decide with the owner: fixed depth (Tab → Category → Command) vs. arbitrarily nested categories (self-referencing parent). Start with the simplest that meets needs.
- Examples/notes may contain Markdown — render with the same sanitized renderer as NTT.

## Interfaces
- Standalone for now. Possible future: AIM explaining a saved command; PTM counting commands added.
