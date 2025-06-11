# Kubernetes Context Manager

A simple and elegant GUI application for managing Kubernetes contexts on Linux and macOS systems.

[![Build and Release](https://github.com/suslmk-lee/kube-context/actions/workflows/build-release.yml/badge.svg)](https://github.com/suslmk-lee/kube-context/actions/workflows/build-release.yml)

## Features

- 📋 **View & Manage Contexts**: Display, switch, rename, and delete Kubernetes contexts in a clean table format.
- ⭐ **Current Context Indicator**: Clearly shows the active context.
- 🔄 **Seamless Context Switching**: Double-click or use the button to switch contexts instantly.
- 📁 **Import Contexts**: Add contexts from any kubeconfig file via a file dialog.
- ✨ **Naver Cloud (NKS) Integration**: Automatically add contexts for NKS clusters using `ncp-iam-authenticator`.
- 💾 **Automatic Backup**: Creates a backup of your `~/.kube/config` file before making any changes.
- 🎨 **Modern UI**: Clean and intuitive interface built with **PySide6** for a native look and feel on both Linux and macOS.
- 📦 **Automated Builds**: New releases for Linux and macOS are automatically built and published via GitHub Actions.

## Screenshots

*(Screenshots of the new PySide6 interface can be added here)*

## Requirements

- Python 3.7 or higher
- `ncp-iam-authenticator` (Optional, for NKS integration). See [official installation guide](https://guide.ncloud-docs.com/docs/k8s-iam-k8s-iam-auth).

## Installation

### Recommended: Download from Releases

The easiest way to get started is to download the latest pre-built executable for your operating system from the [**GitHub Releases page**](https://github.com/suslmk-lee/kube-context/releases/latest).

1.  Go to the [Releases page](https://github.com/suslmk-lee/kube-context/releases/latest).
2.  Download the asset for your OS (`KubeContextManager-Linux` or `KubeContextManager-macOS.zip`).
3.  **On Linux**: Make the file executable: `chmod +x KubeContextManager-Linux`.
4.  **On macOS**: Unzip the file and run the `KubeContextManager.app`.

### Command Line Download (Linux)

You can also download and run the application directly from your terminal:

```bash
# Replace vX.Y.Z with the latest version from the releases page
VERSION="v0.1.0"

# Download using wget
wget -O KubeContextManager https://github.com/suslmk-lee/kube-context/releases/download/${VERSION}/KubeContextManager-Linux

# Or download using curl
# curl -L -o KubeContextManager https://github.com/suslmk-lee/kube-context/releases/download/${VERSION}/KubeContextManager-Linux

# Make it executable
chmod +x KubeContextManager

# Run the application
./KubeContextManager
```

### Manual Installation (from source)

1.  Clone the repository:
    ```bash
    git clone https://github.com/suslmk-lee/kube-context.git
    cd kube-context
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    python run.py
    ```

## Usage

- **Switch Context**: Double-click a context or select it and click "Switch".
- **Rename Context**: Select a context and click "Rename".
- **Import from File**: Click "Import" to select a `kubeconfig` file to merge.
- **Add NKS Context**: Click "Add NKS" to open a dialog for adding a Naver Cloud Kubernetes Service context.
- **Delete Context**: Select a context and click "Delete".

## Development & Building

This project uses `PyInstaller` to create executables. The build process is automated with GitHub Actions.

To build the application locally:

1.  Install build dependencies:
    ```bash
    pip install pyinstaller
    ```

2.  Run the build script:
    ```bash
    chmod +x build.sh
    ./build.sh
    ```
    The executable will be created in the `dist/` directory.

## Contributing

Contributions, issues, and feature requests are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is open source and available under the MIT License.