#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from kube_config_manager import KubeConfigManager


class KubeContextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kubernetes Context Manager")
        self.root.geometry("900x700")
        
        # Initialize the config manager
        self.config_manager = KubeConfigManager()
        
        # Create main UI
        self.create_widgets()
        
        # Load initial data
        # self.root.after(100, self.refresh_contexts) # Temporarily disabled for Listbox direct test
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # --- MINIMAL LISTBOX TEST START ---
        # This code bypasses the original widget creation to test Listbox in isolation.
        
        # Main frame for testing - give it a visible background
        test_main_frame = tk.Frame(self.root, bg='lightcoral') # Changed color for visibility
        test_main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(test_main_frame, text="Minimal Listbox Isolation Test", font=('Arial', 18, 'bold'), bg='lightcoral').pack(pady=10)

        # Listbox frame for testing - give it a visible background
        test_listbox_frame = tk.Frame(test_main_frame, bg='skyblue') # Changed color for visibility
        test_listbox_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.test_listbox = tk.Listbox(test_listbox_frame, font=('Arial', 14), 
                                         selectmode=tk.SINGLE, height=10, bg='lightyellow')
        test_scrollbar = tk.Scrollbar(test_listbox_frame, orient=tk.VERTICAL, command=self.test_listbox.yview)
        self.test_listbox.configure(yscrollcommand=test_scrollbar.set)
        
        self.test_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        test_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add test items directly
        for i in range(10):
            self.test_listbox.insert(tk.END, f"Hardcoded Test Item {i+1}")
            # Alternate background colors for items for better visibility
            item_bg = 'white' if i % 2 == 0 else '#f0f0f0' # Light gray
            self.test_listbox.itemconfig(i, {'bg': item_bg, 'fg': 'black'})

        print("DEBUG: Minimal create_widgets executed. test_listbox should contain hardcoded items.")
        
        # Initialize other instance variables that might be expected by other parts of the class, to prevent AttributeErrors.
        self.contexts_data = []
        self.current_context_var = tk.StringVar()
        self.current_context_var.set("N/A - Minimal Test")
        # self.current_context_label = tk.Label(test_main_frame, textvariable=self.current_context_var) # Not creating original label
        self.status_var = tk.StringVar()
        self.status_var.set("Minimal Listbox Test Mode - Check for yellow Listbox with items.")
        
        # Ensure other buttons (if accessed as instance vars elsewhere) are at least None
        self.switch_btn = None
        self.delete_btn = None

        return # IMPORTANT: Bypass the rest of the original create_widgets method
        # --- MINIMAL LISTBOX TEST END ---

        # Main frame
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Kubernetes Context Manager", 
                              font=('Arial', 18, 'bold'), bg='white', fg='#333333')
        title_label.pack(pady=(0, 20))
        
        # Current context frame
        current_frame = tk.Frame(main_frame, bg='white')
        current_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(current_frame, text="Current Context:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#555555').pack(side=tk.LEFT)
        
        self.current_context_var = tk.StringVar()
        self.current_context_label = tk.Label(current_frame, textvariable=self.current_context_var,
                                             font=('Arial', 12, 'bold'), bg='white', fg='#2e7d32')
        self.current_context_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Context list frame
        list_frame = tk.Frame(main_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # List label
        tk.Label(list_frame, text="Available Contexts:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#555555').pack(anchor=tk.W)
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg='white')
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.context_listbox = tk.Listbox(listbox_frame, font=('Arial', 12), 
                                         selectmode=tk.SINGLE, height=15, bg='lightyellow')
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.context_listbox.yview)
        self.context_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.context_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click
        self.context_listbox.bind('<Double-Button-1>', self.on_context_double_click)
        self.context_listbox.bind('<<ListboxSelect>>', self.on_context_select)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Buttons
        self.switch_btn = tk.Button(button_frame, text="Switch to Selected Context",
                                   command=self.switch_context, bg='#2e7d32', fg='white',
                                   font=('Arial', 10, 'bold'), state=tk.DISABLED)
        self.switch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        import_btn = tk.Button(button_frame, text="Import Context from File",
                              command=self.import_context, bg='#1976d2', fg='white',
                              font=('Arial', 10))
        import_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = tk.Button(button_frame, text="Delete Selected Context",
                                   command=self.delete_context, bg='#d32f2f', fg='white',
                                   font=('Arial', 10), state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = tk.Button(button_frame, text="Refresh",
                               command=self.refresh_contexts, bg='#757575', fg='white',
                               font=('Arial', 10))
        refresh_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                             font=('Arial', 9), bg='#f5f5f5', fg='#666666',
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(15, 0))
        
        # Store context data
        self.contexts_data = []
    
    def refresh_contexts(self):
        """Refresh the context list."""
        try:
            print("DEBUG: Starting refresh_contexts()")
            self.status_var.set("Loading contexts...")
            
            # Clear existing items
            self.context_listbox.delete(0, tk.END)
            self.contexts_data = []
            
            # Get contexts
            contexts = self.config_manager.get_contexts()
            current_context = self.config_manager.get_current_context()
            
            print(f"DEBUG: Found {len(contexts)} contexts")
            print(f"DEBUG: Current context: {current_context}")
            
            # Update current context display
            if current_context:
                self.current_context_var.set(current_context)
            else:
                self.current_context_var.set("None")
            
            # Populate listbox
            for context in contexts:
                name = context['name']
                cluster = context['context'].get('cluster', '')
                user = context['context'].get('user', '')
                namespace = context['context'].get('namespace', 'default')
                
                # Store context data
                self.contexts_data.append({
                    'name': name,
                    'cluster': cluster,
                    'user': user,
                    'namespace': namespace,
                    'is_current': name == current_context
                })
                
                # Simplified display text and explicit coloring
                display_text = name # Simplest text
                
                self.context_listbox.insert(tk.END, display_text)
                idx = self.context_listbox.size() - 1 # Index of the item just added
                
                if name == current_context:
                    self.context_listbox.itemconfig(idx, {'bg': 'lightgreen', 'fg': 'black'})
                else:
                    self.context_listbox.itemconfig(idx, {'bg': 'white', 'fg': 'black'})
                
                print(f"DEBUG: Added to Listbox: {name} at index {idx}") # Updated debug message
            
            self.status_var.set(f"Loaded {len(contexts)} contexts")
            print("DEBUG: refresh_contexts() completed successfully")
            
        except Exception as e:
            print(f"DEBUG: Error in refresh_contexts(): {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load contexts:\n{str(e)}")
            self.status_var.set("Error loading contexts")
    
    def on_context_select(self, event):
        """Handle context selection."""
        selection = self.context_listbox.curselection()
        if selection:
            self.switch_btn.configure(state=tk.NORMAL)
            self.delete_btn.configure(state=tk.NORMAL)
        else:
            self.switch_btn.configure(state=tk.DISABLED)
            self.delete_btn.configure(state=tk.DISABLED)
    
    def on_context_double_click(self, event):
        """Handle double-click on context."""
        self.switch_context()
    
    def switch_context(self):
        """Switch to the selected context."""
        selection = self.context_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a context to switch to.")
            return
        
        try:
            index = selection[0]
            context_name = self.contexts_data[index]['name']
            
            self.config_manager.set_current_context(context_name)
            self.refresh_contexts()
            
            messagebox.showinfo("Success", f"Switched to context: {context_name}")
            self.status_var.set(f"Switched to context: {context_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch context:\n{str(e)}")
            self.status_var.set("Error switching context")
    
    def import_context(self):
        """Import context from a file."""
        file_path = filedialog.askopenfilename(
            title="Select Kubeconfig File",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set("Importing context...")
                success = self.config_manager.add_context_from_file(file_path)
                
                if success:
                    self.refresh_contexts()
                    messagebox.showinfo("Success", "Context imported successfully!")
                    self.status_var.set("Context imported successfully")
                else:
                    messagebox.showerror("Error", "Failed to import context from file.")
                    self.status_var.set("Failed to import context")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import context:\n{str(e)}")
                self.status_var.set("Error importing context")
    
    def delete_context(self):
        """Delete the selected context."""
        selection = self.context_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a context to delete.")
            return
        
        index = selection[0]
        context_name = self.contexts_data[index]['name']
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Deletion", 
                                   f"Are you sure you want to delete context '{context_name}'?\n\n"
                                   f"This will also remove associated cluster and user if they are not used by other contexts.")
        
        if result:
            try:
                success = self.config_manager.delete_context(context_name)
                
                if success:
                    self.refresh_contexts()
                    messagebox.showinfo("Success", f"Context '{context_name}' deleted successfully!")
                    self.status_var.set(f"Deleted context: {context_name}")
                else:
                    messagebox.showerror("Error", f"Failed to delete context '{context_name}'.")
                    self.status_var.set("Error deleting context")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete context:\n{str(e)}")
                self.status_var.set("Error deleting context")


def main():
    """Main function to run the application."""
    # Suppress macOS Tkinter deprecation warning
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    root = tk.Tk()
    app = KubeContextGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()