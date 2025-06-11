#!/bin/bash

# This script builds the Kubernetes Context Manager application into a single executable file.
# It detects the operating system and adjusts the build process accordingly.

# App name
APP_NAME="KubeContextManager"

# Entry point script
ENTRY_POINT="run.py"

# Detect OS
OS="$(uname)"

PYINSTALLER_OPTS=(
    --name "$APP_NAME"
    --onefile
    --windowed
    --hidden-import="PySide6.QtSvg"
    --hidden-import="PySide6.QtWidgets"
    --hidden-import="PySide6.QtGui"
    --hidden-import="PySide6.QtCore"
)

echo "========================================"
echo "Building $APP_NAME for $OS..."
echo "========================================"

# Clean up previous builds
rm -rf build/ dist/ "$APP_NAME.spec"

# Run PyInstaller with platform-specific options
pyinstaller "${PYINSTALLER_OPTS[@]}" "$ENTRY_POINT"

# Check if the build was successful
BUILD_SUCCESS=false
if [ "$OS" == "Darwin" ]; then
    # On macOS, check for the .app bundle
    if [ -d "dist/$APP_NAME.app" ]; then
        BUILD_SUCCESS=true
    fi
elif [ "$OS" == "Linux" ]; then
    # On Linux, check for the executable file
    if [ -f "dist/$APP_NAME" ]; then
        BUILD_SUCCESS=true
    fi
fi

if [ "$BUILD_SUCCESS" = true ]; then
    echo "========================================"
    echo "Build successful!"
    echo "Executable created in the 'dist' directory."
    echo "========================================"
else
    echo "========================================"
    echo "Build failed. Please check the output above for errors."
    echo "========================================"
fi
