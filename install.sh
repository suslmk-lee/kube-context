#!/bin/bash

set -e

echo "Installing Kubernetes Context Manager..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Make the run script executable
chmod +x run.py

# Create desktop entry for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/kube-context-manager.desktop"
    CURRENT_DIR="$(pwd)"
    
    echo "Creating desktop entry..."
    mkdir -p "$HOME/.local/share/applications"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Name=Kubernetes Context Manager
Comment=Manage Kubernetes contexts with a GUI
Exec=python3 ${CURRENT_DIR}/run.py
Icon=applications-system
Terminal=false
Type=Application
Categories=System;Development;
StartupNotify=true
EOF
    
    echo "Desktop entry created at: $DESKTOP_FILE"
fi

# Create a symlink in /usr/local/bin for command line access
if [[ -w "/usr/local/bin" ]]; then
    echo "Creating command line launcher..."
    ln -sf "$(pwd)/run.py" "/usr/local/bin/kube-context-manager"
    echo "You can now run 'kube-context-manager' from anywhere in the terminal"
elif [[ -w "$HOME/.local/bin" ]]; then
    echo "Creating command line launcher in ~/.local/bin..."
    mkdir -p "$HOME/.local/bin"
    ln -sf "$(pwd)/run.py" "$HOME/.local/bin/kube-context-manager"
    echo "You can now run 'kube-context-manager' from anywhere in the terminal"
    echo "Make sure ~/.local/bin is in your PATH"
fi

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "How to run:"
echo "  1. Double-click the desktop entry (Linux)"
echo "  2. Run 'kube-context-manager' in terminal"
echo "  3. Run 'python3 run.py' from this directory"
echo ""
echo "The application will manage your ~/.kube/config file."
echo "A backup will be created automatically before any changes."