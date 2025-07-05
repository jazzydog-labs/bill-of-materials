#!/usr/bin/env python3
"""
Integration Quality Analyzer for bill-of-materials repository.

This script analyzes the integration quality of repositories in the ecosystem
and identifies gaps in documentation and context files.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import sys


def load_ecosystem(bom_path: str = "bill-of-materials/repos.yaml") -> Dict:
    """Load the ecosystem configuration from repos.yaml."""
    with open(bom_path) as f:
        return yaml.safe_load(f)


def analyze_integration_quality(ecosystem: Dict) -> Dict:
    """Analyze integration quality across all repositories."""
    analysis = {
        "summary": {},
        "repositories": {},
        "gaps": [],
        "recommendations": []
    }
    
    # Initialize counters
    quality_counts = defaultdict(int)
    completeness_counts = defaultdict(int)
    coverage_counts = defaultdict(int)
    
    for repo in ecosystem['repos']:
        repo_name = repo['name']
        quality = repo.get('integration_quality', {})
        
        # Count quality metrics
        if 'documentation_completeness' in quality:
            completeness_counts[quality['documentation_completeness']] += 1
        if 'bom_integration' in quality:
            quality_counts[quality['bom_integration']] += 1
        if 'context_file_coverage' in quality:
            coverage_counts[quality['context_file_coverage']] += 1
        
        # Analyze individual repository
        repo_analysis = analyze_repository(repo)
        analysis["repositories"][repo_name] = repo_analysis
        
        # Identify gaps
        gaps = identify_gaps(repo)
        if gaps:
            analysis["gaps"].extend(gaps)
    
    # Generate summary
    analysis["summary"] = {
        "total_repositories": len(ecosystem['repos']),
        "documentation_completeness": dict(completeness_counts),
        "bom_integration": dict(quality_counts),
        "context_file_coverage": dict(coverage_counts)
    }
    
    # Generate recommendations
    analysis["recommendations"] = generate_recommendations(analysis)
    
    return analysis


def analyze_repository(repo: Dict) -> Dict:
    """Analyze a single repository's integration quality."""
    analysis = {
        "name": repo['name'],
        "type": repo.get('type', 'unknown'),
        "quality": repo.get('integration_quality', {}),
        "documentation_files": 0,
        "context_files": 0,
        "missing_elements": []
    }
    
    # Count documentation files
    docs = repo.get('documentation', {})
    for category in docs.values():
        if isinstance(category, list):
            analysis["documentation_files"] += len(category)
        elif isinstance(category, str):
            analysis["documentation_files"] += 1
    
    # Count context files
    context = repo.get('context_files', {})
    for category in context.values():
        if isinstance(category, list):
            analysis["context_files"] += len(category)
    
    # Identify missing elements
    if not docs.get('readme'):
        analysis["missing_elements"].append("README file")
    
    if not context:
        analysis["missing_elements"].append("context files")
    
    if not repo.get('integration_quality'):
        analysis["missing_elements"].append("integration quality metadata")
    
    return analysis


def identify_gaps(repo: Dict) -> List[Dict]:
    """Identify specific gaps in a repository's integration."""
    gaps = []
    repo_name = repo['name']
    quality = repo.get('integration_quality', {})
    
    # Check documentation completeness
    completeness = quality.get('documentation_completeness', 'missing')
    if completeness in ['minimal', 'missing']:
        gaps.append({
            "repository": repo_name,
            "type": "documentation",
            "severity": "high" if completeness == 'missing' else "medium",
            "description": f"Repository has {completeness} documentation",
            "recommendation": "Add comprehensive README, architecture docs, and usage guides"
        })
    
    # Check context file coverage
    coverage = quality.get('context_file_coverage', 'none')
    if coverage in ['minimal', 'none']:
        gaps.append({
            "repository": repo_name,
            "type": "context_files",
            "severity": "high" if coverage == 'none' else "medium",
            "description": f"Repository has {coverage} context file coverage",
            "recommendation": "Add key config files, source code, and examples for AI tools"
        })
    
    # Check for missing context file categories
    context = repo.get('context_files', {})
    missing_categories = []
    if not context.get('config'):
        missing_categories.append("configuration files")
    if not context.get('code'):
        missing_categories.append("key source code")
    if not context.get('examples'):
        missing_categories.append("examples and usage patterns")
    
    if missing_categories:
        gaps.append({
            "repository": repo_name,
            "type": "context_structure",
            "severity": "medium",
            "description": f"Missing context file categories: {', '.join(missing_categories)}",
            "recommendation": f"Add {', '.join(missing_categories)} to context_files section"
        })
    
    return gaps


def generate_recommendations(analysis: Dict) -> List[str]:
    """Generate actionable recommendations based on analysis."""
    recommendations = []
    
    summary = analysis["summary"]
    
    # Documentation recommendations
    if summary["documentation_completeness"].get('minimal', 0) > 0:
        recommendations.append(
            f"📝 {summary['documentation_completeness']['minimal']} repositories have minimal documentation. "
            "Consider adding comprehensive README files and architecture documentation."
        )
    
    if summary["documentation_completeness"].get('missing', 0) > 0:
        recommendations.append(
            f"🚨 {summary['documentation_completeness']['missing']} repositories are missing documentation. "
            "This is a critical gap that should be addressed immediately."
        )
    
    # Context file recommendations
    if summary["context_file_coverage"].get('minimal', 0) > 0:
        recommendations.append(
            f"🔧 {summary['context_file_coverage']['minimal']} repositories have minimal context file coverage. "
            "Add key configuration files, source code, and examples for better AI tool integration."
        )
    
    if summary["context_file_coverage"].get('none', 0) > 0:
        recommendations.append(
            f"⚠️  {summary['context_file_coverage']['none']} repositories have no context file coverage. "
            "This severely limits AI tool effectiveness."
        )
    
    # Overall ecosystem recommendations
    total_repos = summary["total_repositories"]
    excellent_docs = summary["documentation_completeness"].get('excellent', 0)
    excellent_coverage = summary["context_file_coverage"].get('comprehensive', 0)
    
    if excellent_docs < total_repos * 0.5:
        recommendations.append(
            "🎯 Less than 50% of repositories have excellent documentation. "
            "Consider establishing documentation standards and review processes."
        )
    
    if excellent_coverage < total_repos * 0.3:
        recommendations.append(
            "🤖 Less than 30% of repositories have comprehensive context file coverage. "
            "This limits AI tool effectiveness across the ecosystem."
        )
    
    return recommendations


def print_analysis(analysis: Dict) -> None:
    """Print a formatted analysis report."""
    print("🔍 Foundry Ecosystem Integration Quality Analysis")
    print("=" * 60)
    
    # Summary
    summary = analysis["summary"]
    print(f"\n📊 Summary ({summary['total_repositories']} repositories):")
    print(f"   Documentation Completeness: {dict(summary['documentation_completeness'])}")
    print(f"   BOM Integration: {dict(summary['bom_integration'])}")
    print(f"   Context File Coverage: {dict(summary['context_file_coverage'])}")
    
    # Repository details
    print(f"\n📁 Repository Details:")
    for repo_name, repo_analysis in analysis["repositories"].items():
        quality = repo_analysis["quality"]
        print(f"   {repo_name} ({repo_analysis['type']}):")
        print(f"     Documentation: {quality.get('documentation_completeness', 'unknown')}")
        print(f"     Context Coverage: {quality.get('context_file_coverage', 'unknown')}")
        print(f"     Files: {repo_analysis['documentation_files']} docs, {repo_analysis['context_files']} context")
        
        if repo_analysis["missing_elements"]:
            print(f"     Missing: {', '.join(repo_analysis['missing_elements'])}")
    
    # Gaps
    if analysis["gaps"]:
        print(f"\n🚨 Identified Gaps ({len(analysis['gaps'])}):")
        for gap in analysis["gaps"]:
            severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(gap["severity"], "⚪")
            print(f"   {severity_icon} {gap['repository']}: {gap['description']}")
            print(f"      → {gap['recommendation']}")
    
    # Recommendations
    if analysis["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"   {rec}")
    
    print(f"\n🎉 Analysis complete!")


def main():
    """Main analysis function."""
    try:
        # Load ecosystem
        ecosystem = load_ecosystem()
        
        # Analyze integration quality
        analysis = analyze_integration_quality(ecosystem)
        
        # Print results
        print_analysis(analysis)
        
    except FileNotFoundError:
        print("❌ Error: bill-of-materials/repos.yaml not found")
        print("   Make sure you're running this from the foundry root directory")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 