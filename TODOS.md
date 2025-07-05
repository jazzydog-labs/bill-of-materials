# TODOS for Bill of Materials

This document tracks planned improvements and enhancements for the bill-of-materials repository.

## 🎯 High Priority

### Source of Truth Integration
- [ ] **Individual Repository Metadata Files**
  - Each repository should have a `bom.yaml` or `.bom.yaml` file in its root
  - This file contains self-declared metadata (description, type, context files, etc.)
  - Bill-of-materials aggregates these files rather than maintaining everything centrally
  - Allows repositories to own their own metadata and keep it current

- [ ] **Commit Locking Strategy**
  - Reference specific commits for each repository in the BOM
  - Acts as a "lock file" for the entire ecosystem state
  - Enables reproducible ecosystem snapshots
  - Allows for ecosystem-wide rollbacks and version pinning
  - Example structure:
    ```yaml
    repos:
      - name: loom
        path: ~/dev/jazzydog-labs/foundry/loom
        commit: abc123def456...  # Specific commit hash
        metadata_source: .bom.yaml  # File to read from repo
        last_sync: "2025-01-27T10:30:00Z"
    ```

### Automation Improvements
- [ ] **Automated BOM Updates**
  - Script to pull latest metadata from all repositories
  - Validate that referenced commits still exist
  - Update integration quality metrics automatically
  - Generate diff reports for ecosystem changes

- [ ] **Validation Pipeline**
  - Ensure all referenced files actually exist in repositories
  - Check that commit hashes are valid
  - Validate schema compliance of individual `bom.yaml` files
  - Report on stale or missing metadata

## 🔧 Medium Priority

### Enhanced Schema
- [ ] **Repository Dependencies**
  - Track which repositories depend on others
  - Enable dependency resolution and ordering
  - Support for circular dependency detection

- [ ] **Health Checks**
  - Repository availability status
  - Build/test status integration
  - Security vulnerability tracking
  - Performance metrics

- [ ] **Remote Services Support**
  - Add `type: service` for deployed components
  - Include host information and endpoints
  - Track service health and availability

### Tooling Enhancements
- [ ] **BOM CLI Tool**
  - `bom update` - Pull latest metadata from all repos
  - `bom lock` - Pin all repos to current commits
  - `bom unlock` - Allow repos to update to latest
  - `bom validate` - Check ecosystem health
  - `bom diff` - Show changes between ecosystem states

- [ ] **Integration with Existing Tools**
  - Loom integration for automatic BOM updates
  - CI/CD pipeline integration
  - IDE plugins for BOM awareness

## 📋 Low Priority

### Documentation and Examples
- [ ] **Template Repository**
  - Create a template with example `bom.yaml`
  - Include best practices for metadata organization
  - Provide migration guide from current approach

- [ ] **Migration Strategy**
  - Plan for transitioning from centralized to distributed metadata
  - Backward compatibility considerations
  - Rollout strategy across existing repositories

### Advanced Features
- [ ] **Ecosystem Snapshots**
  - Save complete ecosystem state with commit hashes
  - Enable ecosystem-wide rollbacks
  - Support for multiple ecosystem versions

- [ ] **Analytics and Reporting**
  - Track ecosystem growth over time
  - Identify patterns in repository evolution
  - Generate ecosystem health reports

## 🚧 Implementation Notes

### Individual Repository `bom.yaml` Structure
See `examples/repository-bom-example.yaml` for a complete example.

```yaml
# .bom.yaml in each repository
name: repository-name
description: Human-readable description
type: category
documentation:
  readme: README.md
  architecture:
    - docs/architecture.md
context_files:
  config:
    - config.yaml
  code:
    - src/main.py
  examples:
    - examples/usage.py
integration_quality:
  documentation_completeness: excellent
  context_file_coverage: comprehensive
  last_updated: "2025-01-27"
```

### Benefits of This Approach
1. **Single Source of Truth**: Each repo owns its metadata
2. **Version Locking**: Reproducible ecosystem states
3. **Automation Friendly**: Easy to script updates
4. **Scalable**: Works as ecosystem grows
5. **Self-Documenting**: Repos declare their own purpose and structure

### Migration Considerations
- Start with a few repositories as pilots
- Maintain backward compatibility during transition
- Provide tools to help repositories create their `bom.yaml` files
- Gradually migrate from centralized to distributed approach

## 📝 Notes

- This approach moves from "centralized declaration" to "distributed declaration with central aggregation"
- Commit locking provides stability while allowing controlled updates
- Individual `bom.yaml` files make repositories more self-aware and maintainable
- The bill-of-materials becomes more of a "registry" than a "manifest" 