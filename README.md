# Kubernetes Context Manager

A simple and elegant GUI application for managing Kubernetes contexts on Linux systems.

## Features

- 📋 **View all contexts**: Display all available Kubernetes contexts in a clean table format
- ⭐ **Current context indicator**: Clearly shows which context is currently active
- 🔄 **Switch contexts**: Double-click or use the button to switch between contexts
- 📁 **Import contexts**: Add contexts from kubeconfig files via file dialog
- 🗑️ **Delete contexts**: Remove contexts and their associated clusters/users
- 🔄 **Auto-refresh**: Keep the context list up to date
- 💾 **Automatic backup**: Creates backups before making any changes
- 🎨 **Modern UI**: Clean and intuitive interface built with Tkinter

## Screenshots

The application features a modern, two-panel interface:
- Left panel: Context list with current context highlighted
- Right panel: Action buttons and current context information
- Status bar: Shows current operations and config file path

## Requirements

- Python 3.6 or higher
- Linux operating system
- Tkinter (usually included with Python)
- PyYAML library

## Installation

### Quick Install

1. Clone or download this repository
2. Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Install Python dependencies
- Create a desktop entry (Linux)
- Set up command line launcher
- Make the application executable

### Manual Install

1. Install Python dependencies:
```bash
pip3 install --user -r requirements.txt
```

2. Make the script executable:
```bash
chmod +x run.py
```

## Usage

### Running the Application

After installation, you can run the application in several ways:

1. **Desktop Entry** (Linux): Look for "Kubernetes Context Manager" in your applications menu
2. **Command Line**: Run `kube-context-manager` from anywhere in terminal
3. **Direct Execution**: Run `python3 run.py` from the application directory

### Using the Interface

1. **View Contexts**: All available contexts are displayed in the main table
2. **Current Context**: The active context is marked with a ★ symbol
3. **Switch Context**: 
   - Double-click on any context, or
   - Select a context and click "Switch to Selected Context"
4. **Import Context**: 
   - Click "Import Context from File"
   - Select a kubeconfig YAML file
   - The contexts will be merged into your config
5. **Delete Context**:
   - Select a context and click "Delete Selected Context"
   - Associated clusters and users will be removed if not used elsewhere
6. **Refresh**: Click "Refresh" to reload the context list

### Safety Features

- **Automatic Backup**: The application creates a backup at `~/.kube/config.backup` before any changes
- **Validation**: Checks for valid kubeconfig structure before importing
- **Confirmation**: Asks for confirmation before deleting contexts
- **Error Handling**: Graceful error handling with user-friendly messages

## File Structure

```
kube-context01/
├── kube_config_manager.py    # Core kubeconfig management logic
├── kube_context_gui.py       # GUI application
├── run.py                    # Application launcher
├── install.sh               # Installation script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

The application works with your existing `~/.kube/config` file. No additional configuration is needed.

## Troubleshooting

### Common Issues

1. **"Python 3 not found"**: Install Python 3 using your distribution's package manager
2. **"pip3 not found"**: Install pip3: `sudo apt install python3-pip` (Ubuntu/Debian)
3. **Permission denied**: Make sure the script is executable: `chmod +x run.py`
4. **Import fails**: Ensure the kubeconfig file is valid YAML format

### Debug Mode

To run with debug information, set the environment variable:
```bash
export PYTHONPATH=$(pwd)
python3 -u run.py
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Security

This application:
- Only reads and writes to your kubeconfig file
- Creates automatic backups before changes
- Does not send any data over the network
- Runs entirely locally on your machine