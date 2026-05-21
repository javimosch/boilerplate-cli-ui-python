#!/bin/bash
# Build script for agent-first Python CLI using PyInstaller
# Following AGENTS_FRIENDLY_TOOLS.md principles

set -e

echo "Building boilerplate-cli-ui-python with PyInstaller..."

# Install PyInstaller if not already installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build single-file binary
echo "Building single-file binary..."
pyinstaller \
    --onefile \
    --name boilerplate-cli-ui-python \
    --add-data "schemas:schemas" \
    --hidden-import=src \
    --strip \
    --noupx \
    src/main.py

# Move binary to project root
echo "Moving binary to project root..."
mv dist/boilerplate-cli-ui-python .

# Cleanup build artifacts
echo "Cleaning up build artifacts..."
rm -rf build/ dist/ boilerplate-cli-ui-python.spec

# Make binary executable
chmod +x boilerplate-cli-ui-python

# Show binary size
echo ""
echo "Build complete!"
echo "Binary size:"
ls -lh boilerplate-cli-ui-python

# Test binary
echo ""
echo "Testing binary..."
./boilerplate-cli-ui-python version
./boilerplate-cli-ui-python greet --name "Test"

echo ""
echo "Binary ready at: ./boilerplate-cli-ui-python"
echo "Usage examples:"
echo "  ./boilerplate-cli-ui-python greet --name Alice"
echo "  ./boilerplate-cli-ui-python start --port 8080"
echo "  ./boilerplate-cli-ui-python --help-json"