#!/usr/bin/env python3
"""
Example Python consumer for bill-of-materials repository.

This script demonstrates how to load and use the ecosystem configuration
from the bill-of-materials repository.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


def load_ecosystem(bom_path: str = "bill-of-materials/repos.yaml") -> Dict:
    """Load the ecosystem configuration from repos.yaml."""
    with open(bom_path) as f:
        return yaml.safe_load(f)


def get_repo_path(ecosystem: Dict, repo_name: str) -> Optional[Path]:
    """Get the local path for a repository by name."""
    for repo in ecosystem['repos']:
        if repo['name'] == repo_name:
            return Path(repo['path']).expanduser()
    return None


def get_repos_by_type(ecosystem: Dict, repo_type: str) -> List[Dict]:
    """Get all repositories of a specific type."""
    return [repo for repo in ecosystem['repos'] if repo.get('type') == repo_type]


def get_context_files(ecosystem: Dict, repo_name: str) -> List[str]:
    """Get the context files for a repository."""
    for repo in ecosystem['repos']:
        if repo['name'] == repo_name:
            return repo.get('context_files', [])
    return []


def list_all_repos(ecosystem: Dict) -> None:
    """Print all repositories in the ecosystem."""
    print("Foundry Ecosystem Repositories:")
    print("=" * 50)
    
    for repo in ecosystem['repos']:
        print(f"📁 {repo['name']}")
        print(f"   Type: {repo.get('type', 'unknown')}")
        print(f"   Path: {repo['path']}")
        print(f"   Description: {repo['description']}")
        print(f"   Remote: {repo['remotes']['origin']}")
        if repo.get('context_files'):
            print(f"   Context Files: {', '.join(repo['context_files'])}")
        print()


def main():
    """Main example function."""
    try:
        # Load the ecosystem
        ecosystem = load_ecosystem()
        
        # Example 1: List all repositories
        list_all_repos(ecosystem)
        
        # Example 2: Get specific repository path
        loom_path = get_repo_path(ecosystem, "loom")
        if loom_path:
            print(f"🔗 Loom repository path: {loom_path}")
            print(f"   Exists: {loom_path.exists()}")
        
        # Example 3: Get all tooling repositories
        tooling_repos = get_repos_by_type(ecosystem, "tooling")
        print(f"\n🛠️  Tooling repositories ({len(tooling_repos)}):")
        for repo in tooling_repos:
            print(f"   - {repo['name']}: {repo['description']}")
        
        # Example 4: Get context files for a repository
        context_files = get_context_files(ecosystem, "ledger")
        print(f"\n📄 Ledger context files:")
        for file in context_files:
            print(f"   - {file}")
        
        # Example 5: Check repository availability
        print(f"\n🔍 Repository Status:")
        for repo in ecosystem['repos']:
            repo_path = Path(repo['path']).expanduser()
            status = "✅" if repo_path.exists() else "❌"
            print(f"   {status} {repo['name']}: {repo_path}")
            
    except FileNotFoundError:
        print("❌ Error: bill-of-materials/repos.yaml not found")
        print("   Make sure you're running this from the foundry root directory")
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 