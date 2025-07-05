# Bill of Materials

The canonical, read-only source of truth for the full foundry ecosystem layout — defining which repositories exist, their purpose, where they live locally, and any metadata necessary for orchestration, observability, or coordination across tools like `loom` and `panorama`.

## Purpose

- **Declaratively track** all system repositories (e.g. `foundry-bootstrap`, `loom`, `ledger`, `vault`, etc.)
- **Centralize metadata** such as:
  - Local path
  - Remote URL(s)
  - Description
  - Type/category
  - Documentation files (README, architecture, guides)
  - Context files (config, code, tests, examples, data)
  - Integration quality metrics
- **Provide a stable interface** for tools to reference the current system topology
- **Versioned, transparent, and tool-agnostic** configurations (readable by Python, shell, agent tools)

## Structure

```
bill-of-materials/
├── repos.yaml               # Main system definition
├── README.md                # This documentation
├── TODOS.md                 # Future improvements and roadmap
├── schema/                  # JSON schema for validation
│   └── repository.schema.json
└── examples/                # Example usages and analysis tools
    ├── python_consumer.py   # Python ecosystem loader
    ├── shell_consumer.sh    # Shell-based analysis
    ├── integration_analyzer.py # Quality analysis and gap detection
    └── repository-bom-example.yaml # Example individual repo bom.yaml
```

## Format

The main configuration is in `repos.yaml` with this structure:

```yaml
repos:
  - name: repository-name
    path: ~/dev/jazzydog-labs/foundry/repository-name
    description: Human-readable description of the repository's purpose
    remotes:
      origin: https://github.com/jazzydog-labs/repository-name.git
    documentation:
      readme: README.md
      architecture:
        - docs/architecture.md
      guides:
        - docs/usage.md
    context_files:
      config:
        - config.yaml
        - settings.json
      code:
        - src/main.py
        - lib/core.js
      examples:
        - examples/basic_usage.py
    type: category
    integration_quality:
      documentation_completeness: excellent
      bom_integration: complete
      context_file_coverage: comprehensive
      last_updated: "2025-01-27"
      notes: "Additional notes about integration status"
```

### Repository Types

- **bootstrap**: Foundational setup and tooling (e.g., `foundry-bootstrap`)
- **orchestrator**: System coordination and management (e.g., `loom`)
- **design**: Conceptual and modeling work (e.g., `crucible`)
- **generation**: Code creation and scaffolding (e.g., `forge`)
- **storage**: Data persistence and secrets (e.g., `vault`)
- **tracking**: Session and artifact management (e.g., `ledger`)
- **tooling**: Development utilities and aliases (e.g., `just-aliases`)
- **registry**: Metadata and configuration (e.g., `bill-of-materials`)

## Guidelines

- **Read-only**: This repository never runs code or modifies state — it is purely declarative
- **Consumable**: May be consumed by tools via submodule, direct checkout, or raw file access
- **Stable**: Should remain stable, versioned, and independent of runtime workflows
- **Secure**: No secrets or user-specific credentials should be stored
- **Extensible**: Designed to support future additions like remote services or deployed components
- **Best-effort**: Integration quality metrics help identify gaps and areas for improvement
- **Self-documenting**: The BOM itself serves as documentation of ecosystem completeness

## Usage Examples

### Python Consumption

```python
import yaml
from pathlib import Path

def load_ecosystem():
    with open('bill-of-materials/repos.yaml') as f:
        return yaml.safe_load(f)

def get_repo_path(repo_name):
    ecosystem = load_ecosystem()
    for repo in ecosystem['repos']:
        if repo['name'] == repo_name:
            return Path(repo['path']).expanduser()
    return None
```

### Shell Consumption

```bash
# Get all repository paths
yq eval '.repos[].path' bill-of-materials/repos.yaml

# Find repositories by type
yq eval '.repos[] | select(.type == "tooling") | .name' bill-of-materials/repos.yaml
```

### Agent Tool Consumption

```yaml
# Example for AI agents to understand system topology
- name: loom
  path: ~/dev/jazzydog-labs/foundry/loom
  description: Central orchestrator for the foundry ecosystem
  context_files:
    - README.md  # Primary documentation
    - repos.yaml # Configuration
```

## Future Considerations

- **Distributed Metadata**: Individual repository `bom.yaml` files (see [TODOS.md](TODOS.md))
- **Commit Locking**: Version pinning for reproducible ecosystem states
- **Remote Services**: Support for deployed components (e.g., add `type: service` or `host: prod.local`)
- **Dependencies**: Repository dependency relationships and ordering
- **Health Checks**: Repository status and availability information
- **Schema Validation**: Formal schema definition for the YAML structure
- **Change Tracking**: Version history and migration documentation

## Contributing

To add or modify repository definitions:

1. Update `repos.yaml` with the new repository information
2. Ensure all required fields are present (name, path, description, remotes)
3. Add appropriate context files for documentation and AI consumption
4. Update this README if new repository types or patterns are introduced

## Related Tools

- **loom**: Uses this registry for repository orchestration
- **panorama**: (Future) May use this for system observability
- **foundry-bootstrap**: Referenced by this registry for setup information
- **integration_analyzer.py**: Analyzes integration quality and identifies gaps 