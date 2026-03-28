#!/bin/bash
# generate_changelog.sh
# Generates CHANGELOG.md for a new release using git-cliff.
#
# Usage:
#   bash generate_changelog.sh v1.1.0
#
# Prerequisites — install once:
#   # Install Rust/cargo:
#   curl https://sh.rustup.rs -sSf | sh
#   source ~/.cargo/env
#
#   # Install git-cliff:
#   cargo install git-cliff
#
# Commit message conventions for best results:
#   feat: add X        → Added
#   fix: correct Y     → Fixed
#   update: improve Z  → Changed
#   remove: drop W     → Removed
#   doc: update README → Documentation
#   chore: ...         → skipped (won't appear in changelog)

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: bash generate_changelog.sh vX.Y.Z"
    echo "Example: bash generate_changelog.sh v1.1.0"
    exit 1
fi

# Validate format
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: version must be in format vX.Y.Z (e.g. v1.1.0)"
    exit 1
fi

# Check git-cliff is installed
if ! command -v git-cliff &> /dev/null; then
    echo "git-cliff not found. Install it with:"
    echo "  cargo install git-cliff"
    echo ""
    echo "If cargo is not installed:"
    echo "  curl https://sh.rustup.rs -sSf | sh"
    echo "  source ~/.cargo/env"
    echo "  cargo install git-cliff"
    exit 1
fi

echo "Generating CHANGELOG.md for $VERSION..."
git-cliff --tag "$VERSION" -o CHANGELOG.md

echo ""
echo "Done. Review CHANGELOG.md, then run:"
echo ""
echo "  git add CHANGELOG.md"
echo "  git commit -m \"chore: release $VERSION\""
echo "  git tag $VERSION"
echo "  git push && git push --tags"
