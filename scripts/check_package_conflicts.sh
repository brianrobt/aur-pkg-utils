#!/bin/bash

# Enhanced script to check for conflicts in PKGBUILD provides array
# This script checks both the provides array and the package name itself

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PKGBUILD exists
if [[ ! -f "PKGBUILD" ]]; then
    echo -e "${RED}Error: PKGBUILD not found in current directory${NC}"
    exit 1
fi

# Source the PKGBUILD to get variables
source PKGBUILD

echo -e "${GREEN}Checking provides array conflicts for package: ${pkgname}${NC}"
echo "=============================================="

# Function to check if a package/capability exists
check_capability() {
    local capability="$1"
    local source_type="$2"  # "package" or "provides"

    echo -e "\n${YELLOW}Checking ${source_type}: ${capability}${NC}"

    # Use pacman -F to find what provides this capability
    local results=$(pacman -F "$capability" 2>/dev/null || true)

    if [[ -n "$results" ]]; then
        echo -e "${RED}CONFLICT DETECTED!${NC}"
        echo "The following packages already provide '$capability':"
        echo "$results"
        return 1
    else
        echo -e "${GREEN}✓ No conflicts found${NC}"
        return 0
    fi
}

# Check the package name itself
echo -e "\n${YELLOW}=== Checking package name ===${NC}"
check_capability "$pkgname" "package"
pkgname_conflict=$?

# Check provides array if it exists
provides_conflicts=0
if [[ -n "${provides:-}" ]]; then
    echo -e "\n${YELLOW}=== Checking provides array ===${NC}"

    # Parse provides array - handle both array formats
    # Method 1: Try to extract from PKGBUILD directly
    provides_list=""
    if declare -p provides 2>/dev/null | grep -q "declare -a"; then
        # It's an array
        for provide in "${provides[@]}"; do
            provides_list+="$provide "
        done
    else
        # Try regex extraction as fallback
        provides_list=$(grep -oP "provides=\(\K[^)]*" PKGBUILD 2>/dev/null | tr -d "'" | tr -d '"' || true)
    fi

    if [[ -n "$provides_list" ]]; then
        for provide in $provides_list; do
            # Skip empty entries
            [[ -z "$provide" ]] && continue

            # Remove version constraints (e.g., "foo>=1.0" becomes "foo")
            clean_provide=$(echo "$provide" | sed 's/[<>=].*//')

            if ! check_capability "$clean_provide" "provides"; then
                ((provides_conflicts++))
            fi
        done
    else
        echo "No provides array found or empty"
    fi
else
    echo -e "\n${YELLOW}No provides array defined in PKGBUILD${NC}"
fi

# Summary
echo -e "\n${YELLOW}=== SUMMARY ===${NC}"
total_conflicts=$((pkgname_conflict + provides_conflicts))

if [[ $total_conflicts -eq 0 ]]; then
    echo -e "${GREEN}✓ No conflicts detected! Your package name and provides array look good.${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $total_conflicts conflict(s) that need to be resolved.${NC}"
    echo
    echo "Recommendations:"
    echo "1. Choose a different package name if the main package conflicts"
    echo "2. Remove conflicting entries from the provides array"
    echo "3. Check if the conflicting package is abandoned/can be replaced"
    echo "4. Consider using a more specific name (e.g., add suffix like -git, -bin)"
    exit 1
fi