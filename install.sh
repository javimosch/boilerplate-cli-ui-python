#!/bin/bash
# Installation script for boilerplate-cli-ui-python
# Usage: curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/main/install.sh | bash

set -e

VERSION=${1:-latest}
BINARY_NAME="boilerplate-cli-ui-python"
INSTALL_DIR=${INSTALL_DIR:-/usr/local/bin}

echo "Installing ${BINARY_NAME} ${VERSION}..."

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        ARCH="amd64"
    elif [[ "$ARCH" == "aarch64" ]]; then
        ARCH="arm64"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="darwin"
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        ARCH="amd64"
    elif [[ "$ARCH" == "arm64" ]]; then
        ARCH="arm64"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

BINARY="${BINARY_NAME}-${PLATFORM}-${ARCH}"

# Download binary
if [[ "$VERSION" == "latest" ]]; then
    DOWNLOAD_URL="https://github.com/javimosch/${BINARY_NAME}/releases/latest/download/${BINARY}"
else
    DOWNLOAD_URL="https://github.com/javimosch/${BINARY_NAME}/releases/download/${VERSION}/${BINARY}"
fi

echo "Downloading from: $DOWNLOAD_URL"

# Create temp directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# Download binary
curl -sSL -o "${BINARY}" "${DOWNLOAD_URL}"

# Make executable
chmod +x "${BINARY}"

# Install
if [[ -w "$INSTALL_DIR" ]]; then
    mv "${BINARY}" "${INSTALL_DIR}/${BINARY_NAME}"
else
    echo "Installing to ${INSTALL_DIR} requires sudo privileges..."
    sudo mv "${BINARY}" "${INSTALL_DIR}/${BINARY_NAME}"
fi

# Cleanup
cd -
rm -rf "$TMP_DIR"

echo "✓ ${BINARY_NAME} installed successfully to ${INSTALL_DIR}/${BINARY_NAME}"
echo "Run: ${BINARY_NAME} --help"