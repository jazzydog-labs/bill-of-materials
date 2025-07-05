#!/bin/bash
# Example shell consumer for bill-of-materials repository.
#
# This script demonstrates how to load and use the ecosystem configuration
# from the bill-of-materials repository using shell tools like yq v3.

set -euo pipefail

BOM_FILE="bill-of-materials/repos.yaml"

# Check if yq is available (should now use the Go-based version)
if ! command -v yq &> /dev/null; then
    echo "❌ Error: yq is required but not installed"
    echo "   Install with: brew install yq"
    exit 1
fi

# Verify we're using the Go-based yq
if ! yq --version | grep -q "mikefarah/yq"; then
    echo "❌ Error: Go-based yq is required (found Python yq instead)"
    echo "   Install with: brew install yq"
    exit 1
fi

# Check if the BOM file exists
if [[ ! -f "$BOM_FILE" ]]; then
    echo "❌ Error: $BOM_FILE not found"
    echo "   Make sure you're running this from the foundry root directory"
    exit 1
fi

echo "🔍 Foundry Ecosystem Analysis"
echo "=============================="

# Example 1: List all repository names
echo -e "\n📁 All Repositories:"
yq eval '.repos[].name' "$BOM_FILE" | nl

# Example 2: Get all repository paths
echo -e "\n📍 Repository Paths:"
yq eval '.repos[] | .name + ": " + .path' "$BOM_FILE"

# Example 3: Find repositories by type
echo -e "\n🛠️  Tooling Repositories:"
yq eval '.repos[] | select(.type == "tooling") | .name' "$BOM_FILE" | nl

echo -e "\n🎨 Design Repositories:"
yq eval '.repos[] | select(.type == "design") | .name' "$BOM_FILE" | nl

# Example 4: Get repository descriptions
echo -e "\n📝 Repository Descriptions:"
yq eval '.repos[] | .name + ": " + .description' "$BOM_FILE"

# Example 5: Check which repositories exist locally
echo -e "\n🔍 Local Repository Status:"
while IFS= read -r repo_name; do
    while IFS= read -r repo_path; do
        expanded_path=$(eval echo "$repo_path")
        if [[ -d "$expanded_path" ]]; then
            echo "✅ $repo_name: $expanded_path"
        else
            echo "❌ $repo_name: $expanded_path (missing)"
        fi
    done < <(yq eval ".repos[] | select(.name == \"$repo_name\") | .path" "$BOM_FILE")
done < <(yq eval '.repos[].name' "$BOM_FILE")

# Example 6: Get context files for a specific repository
echo -e "\n📄 Context Files for 'ledger':"
yq eval '.repos[] | select(.name == "ledger") | .context_files[]' "$BOM_FILE" 2>/dev/null || echo "   No context files defined"

# Example 7: Count repositories by type
echo -e "\n📊 Repository Type Distribution:"
yq eval '.repos[].type' "$BOM_FILE" | sort | uniq -c | sort -nr

# Example 8: Get remote URLs
echo -e "\n🌐 Remote URLs:"
yq eval '.repos[] | .name + ": " + .remotes.origin' "$BOM_FILE"

# Example 9: Find repositories with specific context files
echo -e "\n📋 Repositories with README.md context:"
yq eval '.repos[] | select(.context_files[] == "README.md") | .name' "$BOM_FILE" | nl

# Example 10: Validate repository structure
echo -e "\n🔧 Repository Structure Validation:"
echo "Checking for required fields..."

required_fields=("name" "path" "description" "remotes")
missing_fields=0

for repo_name in $(yq eval '.repos[].name' "$BOM_FILE"); do
    for field in "${required_fields[@]}"; do
        if ! yq eval ".repos[] | select(.name == \"$repo_name\") | .$field" "$BOM_FILE" >/dev/null 2>&1; then
            echo "❌ $repo_name: missing required field '$field'"
            ((missing_fields++))
        fi
    done
done

if [[ $missing_fields -eq 0 ]]; then
    echo "✅ All repositories have required fields"
else
    echo "❌ Found $missing_fields missing required fields"
fi

echo -e "\n🎉 Analysis complete!" 