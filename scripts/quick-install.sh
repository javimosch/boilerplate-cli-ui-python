#!/bin/bash
# Quick install script for boilerplate-cli-ui-python
# Fast setup for agents - clone and run CLI immediately

set -e

echo "=== Quick installing boilerplate-cli-ui-python ==="

# Clone to temporary directory first
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

echo "Cloning repository..."
git clone https://github.com/javimosch/boilerplate-cli-ui-python.git
cd boilerplate-cli-ui-python

echo "=== Running CLI help ==="
python3 -m src.main --help-json

echo ""
echo "✓ CLI is ready to use!"
echo "Location: $TMP_DIR/boilerplate-cli-ui-python"
echo ""
echo "Quick usage:"
echo "  cd $TMP_DIR/boilerplate-cli-ui-python"
echo "  python3 -m src.main greet --name QuickTest"
echo "  python3 -m src.main version"
echo ""
echo "For permanent installation, run:"
echo "  bash scripts/install-for-agents.sh"

# Keep directory available for testing
echo ""
echo "✓ CLI is ready to use!"
echo "Location: $TMP_DIR/boilerplate-cli-ui-python"
echo ""
echo "Quick usage:"
echo "  cd $TMP_DIR/boilerplate-cli-ui-python"
echo "  python3 -m src.main greet --name QuickTest"
echo "  python3 -m src.main version"
echo ""
echo "For permanent installation, run:"
echo "  bash scripts/install-for-agents.sh"
echo ""
echo "To cleanup temporary directory later:"
echo "  rm -rf $TMP_DIR"