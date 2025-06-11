import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QGroupBox,
    QMessageBox,
    QFileDialog,
    QHeaderView,
    QStatusBar,
    QInputDialog,
    QFormLayout,
    QDialog,
    QLineEdit,
    QDialogButtonBox
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QFont

from kube_config_manager import KubeConfigManager

class KubeContextGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kubernetes Context Manager")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the config manager
        self.config_manager = KubeConfigManager()

        # Create main UI
        self.create_widgets()

        # Connect signals to slots
        self.refresh_btn.clicked.connect(self.refresh_contexts)
        self.import_btn.clicked.connect(self.import_context)
        self.add_nks_btn.clicked.connect(self.add_nks_context_dialog) # Connect new button
        self.rename_btn.clicked.connect(self.rename_context_dialog) # Connect new button
        self.delete_btn.clicked.connect(self.delete_context)
        self.switch_btn.clicked.connect(self.switch_context)
        self.context_tree.itemSelectionChanged.connect(self.on_context_select)
        self.context_tree.itemDoubleClicked.connect(self.switch_context)

        # Load initial data
        self.refresh_contexts()
        self.on_context_select() # Set initial button state

    def create_widgets(self):
        """Create and layout all widgets."""
        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Kubernetes Context Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Main content area (panels)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Left panel - Context list
        self.create_context_panel(content_layout)

        # Right panel - Actions
        self.create_action_panel(content_layout)
        
        # Set stretch factors for panels
        content_layout.setStretch(0, 3) # Context panel takes more space
        content_layout.setStretch(1, 1)

        # Status bar
        self.create_status_bar()

    def create_context_panel(self, parent_layout):
        """Create the context list panel."""
        context_groupbox = QGroupBox("Contexts")
        layout = QVBoxLayout(context_groupbox)
        
        # Create treeview for contexts
        self.context_tree = QTreeWidget()
        self.context_tree.setColumnCount(4)
        self.context_tree.setHeaderLabels(['Context Name', 'Cluster', 'User', 'Namespace'])
        self.context_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.context_tree.header().setStretchLastSection(False)

        layout.addWidget(self.context_tree)
        parent_layout.addWidget(context_groupbox)

    def create_action_panel(self, parent_layout):
        """Create the action buttons panel."""
        action_groupbox = QGroupBox("Actions")
        layout = QVBoxLayout(action_groupbox)
        action_groupbox.setFixedWidth(250)

        # Current context info
        self.current_context_label = QLabel("Current: None")
        font = self.current_context_label.font()
        font.setBold(True)
        self.current_context_label.setFont(font)
        layout.addWidget(self.current_context_label)

        # Action buttons
        self.switch_btn = QPushButton("Switch to Selected Context")
        self.import_btn = QPushButton("Import Context from File")
        self.add_nks_btn = QPushButton("Add NKS Context") # New button
        self.rename_btn = QPushButton("Rename Selected Context") # New button
        self.delete_btn = QPushButton("Delete Selected Context")
        self.refresh_btn = QPushButton("Refresh")

        layout.addWidget(self.switch_btn)
        layout.addWidget(self.import_btn)
        layout.addWidget(self.add_nks_btn) # Add new button to layout
        layout.addWidget(self.rename_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()
        layout.addWidget(self.refresh_btn)

        parent_layout.addWidget(action_groupbox)

    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def refresh_contexts(self):
        """Refresh the context list."""
        try:
            self.status_bar.showMessage("Loading contexts...")
            self.context_tree.clear()

            contexts = self.config_manager.get_contexts()
            current_context = self.config_manager.get_current_context()

            if current_context:
                self.current_context_label.setText(f"Current: {current_context}")
            else:
                self.current_context_label.setText("Current: None")

            for context in contexts:
                name = context['name']
                cluster = context['context'].get('cluster', '')
                user = context['context'].get('user', '')
                namespace = context['context'].get('namespace', 'default')
                
                item = QTreeWidgetItem([name, cluster, user, namespace])
                if name == current_context:
                    font = item.font(0)
                    font.setBold(True)
                    item.setFont(0, font)
                    item.setText(0, f"★ {name}") # Add star indicator
                
                self.context_tree.addTopLevelItem(item)

            self.status_bar.showMessage(f"Loaded {len(contexts)} contexts")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load contexts:\n{str(e)}")
            self.status_bar.showMessage("Error loading contexts")

    def on_context_select(self):
        """Handle context selection to enable/disable buttons."""
        is_selected = bool(self.context_tree.selectedItems())
        self.switch_btn.setEnabled(is_selected)
        self.delete_btn.setEnabled(is_selected)

    def switch_context(self):
        """Switch to the selected context."""
        selected_items = self.context_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a context to switch to.")
            return
        
        try:
            # The name might have a star, so we get the original name from the data
            context_name = selected_items[0].text(0).replace('★ ', '')
            self.config_manager.set_current_context(context_name)
            self.refresh_contexts()
            QTimer.singleShot(10, lambda: QMessageBox.information(self, "Success", f"Switched to context: {context_name}"))
            self.status_bar.showMessage(f"Switched to context: {context_name}")
        except Exception as e:
            QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to switch context:\n{str(e)}"))
            self.status_bar.showMessage("Error switching context")

    def import_context(self):
        """Import context from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Kubeconfig File", "", "YAML files (*.yaml *.yml);;All files (*.*)"
        )
        if file_path:
            try:
                self.status_bar.showMessage("Importing context...")
                success = self.config_manager.add_context_from_file(file_path)
                if success:
                    self.refresh_contexts()
                    QTimer.singleShot(10, lambda: QMessageBox.information(self, "Success", "Context imported successfully!"))
                    self.status_bar.showMessage("Context imported successfully")
                else:
                    QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", "Failed to import context from file."))
                    self.status_bar.showMessage("Failed to import context")
            except Exception as e:
                QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to import context:\n{str(e)}"))
                self.status_bar.showMessage("Error importing context")

    def delete_context(self):
        """Delete the selected context."""
        selected_items = self.context_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a context to delete.")
            return

        context_name = selected_items[0].text(0).replace('★ ', '')
        reply = QMessageBox.question(self, 'Confirm Deletion',
            f"Are you sure you want to delete context '{context_name}'?\n\nThis will also remove associated cluster and user if they are not used by other contexts.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                success = self.config_manager.delete_context(context_name)
                if success:
                    self.refresh_contexts()
                    QTimer.singleShot(10, lambda: QMessageBox.information(self, "Success", f"Context '{context_name}' deleted successfully!"))
                    self.status_bar.showMessage(f"Deleted context: {context_name}")
                else:
                    QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to delete context '{context_name}'."))
                    self.status_bar.showMessage("Error deleting context")
            except Exception as e:
                QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to delete context:\n{str(e)}"))
                self.status_bar.showMessage("Error deleting context")

    def add_nks_context_dialog(self):
        """Show a dialog to get NKS cluster info and add context."""
        # Using a custom dialog for better layout
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Naver Cloud NKS Context")
        form_layout = QFormLayout(dialog)

        uuid_edit = QLineEdit(dialog)
        region_edit = QLineEdit(dialog)
        region_edit.setPlaceholderText("e.g., KR, JP")
        alias_edit = QLineEdit(dialog)
        alias_edit.setPlaceholderText("(Optional) Defaults to Cluster UUID")

        form_layout.addRow("Cluster UUID:", uuid_edit)
        form_layout.addRow("Region:", region_edit)
        form_layout.addRow("Context Alias:", alias_edit)

        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form_layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            cluster_uuid = uuid_edit.text().strip()
            region = region_edit.text().strip().upper()
            alias = alias_edit.text().strip() or None # Use None if empty

            if not cluster_uuid or not region:
                QMessageBox.warning(self, "Input Error", "Cluster UUID and Region are required.")
                return

            try:
                self.status_bar.showMessage(f"Adding NKS context for {cluster_uuid}...")
                # Use the default authenticator path logic within KubeConfigManager
                success, message = self.config_manager.add_nks_context(
                    cluster_uuid, region, alias=alias
                )
                
                if success:
                    self.refresh_contexts()
                    QTimer.singleShot(10, lambda: QMessageBox.information(self, "Success", message))
                    self.status_bar.showMessage(f"NKS context for {cluster_uuid} added/updated.")
                else:
                    QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to add NKS context:\n{message}"))
                    self.status_bar.showMessage("Error adding NKS context.")
            except Exception as e:
                QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}"))
                self.status_bar.showMessage("Unexpected error adding NKS context.")

    def rename_context_dialog(self):
        """Show a dialog to get a new name for the selected context and rename it."""
        selected_items = self.context_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Context Selected", "Please select a context to rename.")
            return

        old_name = selected_items[0].text(0).replace('★ ', '') # Remove current context indicator

        new_name, ok = QInputDialog.getText(self, "Rename Context", 
                                            f"Enter new name for '{old_name}':", 
                                            QLineEdit.Normal, old_name)

        if ok and new_name.strip():
            new_name = new_name.strip()
            if new_name == old_name:
                QMessageBox.information(self, "No Change", "The new name is the same as the old name.")
                return
            
            try:
                self.status_bar.showMessage(f"Renaming context '{old_name}' to '{new_name}'...")
                success, message = self.config_manager.rename_context(old_name, new_name)
                
                if success:
                    self.refresh_contexts()
                    QTimer.singleShot(10, lambda: QMessageBox.information(self, "Success", message))
                    self.status_bar.showMessage(f"Context '{old_name}' renamed to '{new_name}'.")
                else:
                    QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"Failed to rename context:\n{message}"))
                    self.status_bar.showMessage(f"Error renaming context '{old_name}'.")
            except Exception as e:
                QTimer.singleShot(10, lambda: QMessageBox.critical(self, "Error", f"An unexpected error occurred while renaming:\n{str(e)}"))
                self.status_bar.showMessage("Unexpected error renaming context.")
        elif ok and not new_name.strip():
            QMessageBox.warning(self, "Invalid Name", "New context name cannot be empty.")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = KubeContextGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
