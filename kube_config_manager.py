import os
import yaml
import shutil
import tempfile
import subprocess
import platform
import sys
from pathlib import Path
from typing import Dict, List, Optional


class KubeConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.kube/config")
        self.config_dir = os.path.dirname(self.config_path)
        self.backup_path = f"{self.config_path}.backup"
        self._ensure_config_exists()

    def _get_default_ncp_authenticator_path(self):
        """Return the default path for ncp-iam-authenticator, considering PyInstaller bundle."""
        # Check if running in a PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in a bundle
            base_path = sys._MEIPASS
            if platform.system() == "Windows":
                return os.path.join(base_path, 'ncp-iam-authenticator.exe')
            else:
                return os.path.join(base_path, 'ncp-iam-authenticator')

        # Not in a bundle, use standard paths
        if platform.system() == "Windows":
            return os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "ncp-iam-authenticator", "ncp-iam-authenticator.exe")
        else:
            return "/usr/local/bin/ncp-iam-authenticator"

    def check_ncp_authenticator_exists(self, authenticator_path=None):
        """Check if ncp-iam-authenticator exists at the given or default path."""
        path_to_check = authenticator_path or self._get_default_ncp_authenticator_path()
        
        # Try to find in PATH if not found at default/specified absolute path
        if not os.path.exists(path_to_check) and not os.path.isabs(path_to_check):
            found_in_path = shutil.which(path_to_check)
            if found_in_path:
                path_to_check = found_in_path
            else:
                 raise FileNotFoundError(f"'{path_to_check}' not found in PATH or at the specified location. Please install ncp-iam-authenticator or provide the correct path.")
        elif not os.path.exists(path_to_check):
            raise FileNotFoundError(f"ncp-iam-authenticator not found at {path_to_check}. Please install it or provide the correct path.")

        if not os.access(path_to_check, os.X_OK):
            raise PermissionError(f"ncp-iam-authenticator at {path_to_check} is not executable. Please check permissions.")
        return path_to_check

    def add_nks_context(self, cluster_uuid, region, alias=None, authenticator_path=None, kubeconfig_path=None):
        """Add NKS context using ncp-iam-authenticator."""
        try:
            actual_authenticator_path = self.check_ncp_authenticator_exists(authenticator_path)
            
            cmd = [
                actual_authenticator_path,
                "update-kubeconfig",
                "--clusterUuid", cluster_uuid,
                "--region", region
            ]

            if alias:
                cmd.extend(["--alias", alias])
            
            target_kubeconfig = kubeconfig_path or self.config_path
            cmd.extend(["--kubeconfig", target_kubeconfig])

            os.makedirs(os.path.dirname(target_kubeconfig), exist_ok=True)

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                error_message = f"ncp-iam-authenticator failed with error code {process.returncode}:\nSTDERR: {stderr.strip()}\nSTDOUT: {stdout.strip()}"
                if "cluster not found" in stderr.lower():
                     error_message += "\n\nPlease check if the Cluster UUID and Region are correct."
                elif "access denied" in stderr.lower() or "unauthorized" in stderr.lower():
                    error_message += "\n\nPlease check your NCP IAM credentials and permissions."
                elif "no such file or directory" in stderr.lower() and actual_authenticator_path in stderr:
                    error_message = f"ncp-iam-authenticator command failed. It seems the path '{actual_authenticator_path}' is incorrect or the tool is not installed properly.\nSTDERR: {stderr.strip()}"
                raise Exception(error_message)

            # update-kubeconfig command modifies the file directly, so we just need to reload
            # self.load_config() # Reload to reflect changes made by the authenticator - assuming load_config loads self.config_path
            # If target_kubeconfig can be different, we might need to adjust how config is reloaded or managed.
            return True, f"NKS context '{alias or cluster_uuid}' added/updated successfully.\nOutput:\n{stdout.strip()}"
        
        except FileNotFoundError as e:
            return False, str(e)
        except PermissionError as e:
            return False, str(e)
        except Exception as e:
            stderr_msg = stderr.strip() if 'stderr' in locals() and stderr else 'N/A'
            stdout_msg = stdout.strip() if 'stdout' in locals() and stdout else 'N/A'
            return False, f"Error adding NKS context: {str(e)}\nSTDOUT: {stdout_msg}\nSTDERR: {stderr_msg}"

    def rename_context(self, old_name: str, new_name: str) -> tuple[bool, str]:
        """Rename an existing context.

        Args:
            old_name: The current name of the context.
            new_name: The new name for the context.

        Returns:
            A tuple (success_boolean, message_string).
        """
        if not new_name.strip():
            return False, "New context name cannot be empty."
        
        config = self.load_config()
        if not config:
            return False, "Failed to load kubeconfig."

        # Check if new_name already exists
        existing_context_names = [c['name'] for c in config.get('contexts', [])]
        if new_name in existing_context_names:
            return False, f"Context name '{new_name}' already exists."

        context_found = False
        for context_entry in config.get('contexts', []):
            if context_entry.get('name') == old_name:
                context_entry['name'] = new_name
                context_found = True
                break
        
        if not context_found:
            return False, f"Context '{old_name}' not found."

        # Update current-context if it matches old_name
        if config.get('current-context') == old_name:
            config['current-context'] = new_name
        
        if self.save_config(config):
            return True, f"Context '{old_name}' renamed to '{new_name}' successfully."
        else:
            return False, "Failed to save updated kubeconfig."
    
    def _ensure_config_exists(self):
        """Ensure the kube config directory and file exist."""
        os.makedirs(self.config_dir, exist_ok=True)
        if not os.path.exists(self.config_path):
            self._create_empty_config()
    
    def _create_empty_config(self):
        """Create an empty kubeconfig file."""
        empty_config = {
            'apiVersion': 'v1',
            'kind': 'Config',
            'clusters': [],
            'contexts': [],
            'users': [],
            'current-context': ''
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(empty_config, f, default_flow_style=False)
    
    def load_config(self) -> Dict:
        """Load the kubeconfig file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def save_config(self, config: Dict) -> bool:
        """Save the kubeconfig file atomically to prevent data corruption."""
        # Use mkstemp to create a temporary file securely in the same directory
        try:
            fd, temp_path = tempfile.mkstemp(dir=self.config_dir, prefix=f"{os.path.basename(self.config_path)}.")
            
            # Write the new config to the temporary file
            with os.fdopen(fd, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Atomically replace the original file with the new one
            shutil.move(temp_path, self.config_path)
            return True
            
        except Exception as e:
            print(f"Error saving config atomically: {e}")
            # Clean up the temporary file if it still exists from a failed write
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    def get_contexts(self) -> List[Dict]:
        """Get all contexts from the config."""
        config = self.load_config()
        return config.get('contexts', [])
    
    def get_current_context(self) -> str:
        """Get the current active context."""
        config = self.load_config()
        return config.get('current-context', '')
    
    def set_current_context(self, context_name: str):
        """Set the current active context."""
        config = self.load_config()
        contexts = [ctx['name'] for ctx in config.get('contexts', [])]
        
        if context_name not in contexts:
            raise ValueError(f"Context '{context_name}' not found")
        
        config['current-context'] = context_name
        self.save_config(config)
    
    def add_context_from_file(self, file_path: str) -> bool:
        """Add context from another kubeconfig file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_config = yaml.safe_load(f)
            
            if not new_config or not isinstance(new_config, dict):
                return False
            
            current_config = self.load_config()
            
            # Merge clusters, contexts, and users
            for section in ['clusters', 'contexts', 'users']:
                if section in new_config:
                    current_items = current_config.get(section, [])
                    new_items = new_config[section]
                    
                    # Add new items that don't already exist
                    existing_names = {item['name'] for item in current_items}
                    for item in new_items:
                        if item['name'] not in existing_names:
                            current_items.append(item)
                    
                    current_config[section] = current_items
            
            self.save_config(current_config)
            return True
            
        except Exception as e:
            print(f"Error adding context from file: {e}")
            return False
    
    def delete_context(self, context_name: str) -> bool:
        """Delete a context and its associated cluster and user."""
        try:
            config = self.load_config()
            
            # Find the context
            contexts = config.get('contexts', [])
            context_to_delete = None
            
            for ctx in contexts:
                if ctx['name'] == context_name:
                    context_to_delete = ctx
                    break
            
            if not context_to_delete:
                return False
            
            # Remove context
            config['contexts'] = [ctx for ctx in contexts if ctx['name'] != context_name]
            
            # Get cluster and user names from the context
            cluster_name = context_to_delete['context'].get('cluster')
            user_name = context_to_delete['context'].get('user')
            
            # Remove cluster if it's not used by other contexts
            if cluster_name:
                other_clusters = set()
                for ctx in config['contexts']:
                    other_clusters.add(ctx['context'].get('cluster'))
                
                if cluster_name not in other_clusters:
                    config['clusters'] = [c for c in config.get('clusters', []) 
                                        if c['name'] != cluster_name]
            
            # Remove user if it's not used by other contexts
            if user_name:
                other_users = set()
                for ctx in config['contexts']:
                    other_users.add(ctx['context'].get('user'))
                
                if user_name not in other_users:
                    config['users'] = [u for u in config.get('users', []) 
                                     if u['name'] != user_name]
            
            # Clear current-context if it was the deleted one
            if config.get('current-context') == context_name:
                config['current-context'] = ''
            
            self.save_config(config)
            return True
            
        except Exception as e:
            print(f"Error deleting context: {e}")
            return False