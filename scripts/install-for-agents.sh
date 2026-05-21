#!/bin/bash
# Agent installation script for boilerplate-cli-ui-python
# This script downloads and sets up the CLI for agent use

set -e

REPO_URL="https://github.com/javimosch/boilerplate-cli-ui-python.git"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/share/boilerplate-cli-ui-python}"
BINARY_NAME="boilerplate-cli-ui-python"

echo "=== Installing boilerplate-cli-ui-python for agents ==="

# Create installation directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone repository if not exists
if [ ! -d "boilerplate-cli-ui-python" ]; then
    echo "Cloning repository from $REPO_URL"
    git clone "$REPO_URL"
else
    echo "Repository already exists, pulling latest changes"
    cd boilerplate-cli-ui-python
    git pull
fi

cd boilerplate-cli-ui-python

# Create wrapper script
cat > "$BINARY_NAME" << 'EOF'
#!/bin/bash
# Wrapper script for boilerplate-cli-ui-python
cd "$(dirname "$0")"
python3 -m src.main "$@"
EOF

chmod +x "$BINARY_NAME"

# Add to PATH if not already there
WRAPPER_PATH="$INSTALL_DIR/boilerplate-cli-ui-python/$BINARY_NAME"
if [[ ":$PATH:" != *":$INSTALL_DIR/boilerplate-cli-ui-python:"* ]]; then
    echo "Adding to PATH: export PATH=\"$INSTALL_DIR/boilerplate-cli-ui-python:\$PATH\""
    echo "Add this to your shell profile (~/.bashrc or ~/.zshrc)"
fi

# Run help to verify installation
echo "=== Testing installation ==="
python3 -m src.main --help-json

echo ""
echo "✓ Installation complete!"
echo "CLI location: $WRAPPER_PATH"
echo ""
echo "Usage examples:"
echo "  $WRAPPER_PATH greet --name Agent"
echo "  $WRAPPER_PATH version"
echo "  $WRAPPER_PATH --help-json"
echo ""
echo "To use from anywhere, add to PATH:"
echo "  export PATH=\"$INSTALL_DIR/boilerplate-cli-ui-python:\$PATH\""