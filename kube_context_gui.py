#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from kube_config_manager import KubeConfigManager


class KubeContextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kubernetes Context Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the config manager
        self.config_manager = KubeConfigManager()
        
        # Configure style
        self.setup_styles()
        
        # Create main UI
        self.create_widgets()
        
        # Load initial data
        self.root.after(100, self.refresh_contexts)
    
    def setup_styles(self):
        """Setup custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background='#f0f0f0',
                       foreground='#333333')
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       background='#f0f0f0',
                       foreground='#555555')
        
        style.configure('Action.TButton',
                       font=('Arial', 10),
                       padding=(10, 5))
        
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'))
        
        # Treeview styles
        style.configure('Treeview',
                       font=('Arial', 10),
                       rowheight=25)
        
        style.configure('Treeview.Heading',
                       font=('Arial', 11, 'bold'))
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Kubernetes Context Manager", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Context list
        self.create_context_panel(main_frame)
        
        # Right panel - Actions
        self.create_action_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_context_panel(self, parent):
        """Create the context list panel."""
        # Context list frame
        context_frame = ttk.LabelFrame(parent, text="Contexts", padding="10")
        context_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          padx=(0, 10))
        context_frame.columnconfigure(0, weight=1)
        context_frame.rowconfigure(0, weight=1)
        
        # Create treeview for contexts
        columns = ('Name', 'Cluster', 'User', 'Namespace')
        self.context_tree = ttk.Treeview(context_frame, columns=columns, 
                                        show='tree headings', height=15)
        
        # Configure columns
        self.context_tree.column('#0', width=40, minwidth=40, anchor=tk.CENTER)
        self.context_tree.column('Name', width=200, minwidth=150, anchor=tk.W)
        self.context_tree.column('Cluster', width=200, minwidth=150, anchor=tk.W)
        self.context_tree.column('User', width=150, minwidth=100, anchor=tk.W)
        self.context_tree.column('Namespace', width=150, minwidth=100, anchor=tk.W)
        
        # Configure headings
        self.context_tree.heading('#0', text='')
        self.context_tree.heading('Name', text='Context Name')
        self.context_tree.heading('Cluster', text='Cluster')
        self.context_tree.heading('User', text='User')
        self.context_tree.heading('Namespace', text='Namespace')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(context_frame, orient=tk.VERTICAL, 
                                 command=self.context_tree.yview)
        self.context_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the treeview and scrollbar
        self.context_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click event
        self.context_tree.bind('<Double-1>', self.on_context_double_click)
    
    def create_action_panel(self, parent):
        """Create the action buttons panel."""
        action_frame = ttk.LabelFrame(parent, text="Actions", padding="10")
        action_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Current context info
        current_frame = ttk.Frame(action_frame)
        current_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        current_frame.columnconfigure(1, weight=1)
        
        ttk.Label(current_frame, text="Current Context:", 
                 style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.current_context_var = tk.StringVar()
        current_context_label = ttk.Label(current_frame, textvariable=self.current_context_var,
                                         font=('Arial', 11, 'bold'),
                                         foreground='#2e7d32')
        current_context_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Action buttons
        button_frame = ttk.Frame(action_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        
        # Switch context button
        self.switch_btn = ttk.Button(button_frame, text="Switch to Selected Context",
                                    command=self.switch_context, style='Primary.TButton')
        self.switch_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Separator
        ttk.Separator(button_frame, orient='horizontal').grid(row=1, column=0, 
                                                             sticky=(tk.W, tk.E), pady=10)
        
        # Import context button
        import_btn = ttk.Button(button_frame, text="Import Context from File",
                               command=self.import_context, style='Action.TButton')
        import_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Delete context button
        self.delete_btn = ttk.Button(button_frame, text="Delete Selected Context",
                                    command=self.delete_context, style='Action.TButton')
        self.delete_btn.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Separator
        ttk.Separator(button_frame, orient='horizontal').grid(row=4, column=0, 
                                                             sticky=(tk.W, tk.E), pady=10)
        
        # Refresh button
        refresh_btn = ttk.Button(button_frame, text="Refresh",
                                command=self.refresh_contexts, style='Action.TButton')
        refresh_btn.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Initially disable context-dependent buttons
        self.switch_btn.configure(state='disabled')
        self.delete_btn.configure(state='disabled')
        
        # Bind treeview selection event
        self.context_tree.bind('<<TreeviewSelect>>', self.on_context_select)
    
    def create_status_bar(self, parent):
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                         pady=(20, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                font=('Arial', 9),
                                foreground='#666666')
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Config file path
        config_path = self.config_manager.config_path
        path_label = ttk.Label(status_frame, text=f"Config: {config_path}",
                              font=('Arial', 9),
                              foreground='#888888')
        path_label.grid(row=0, column=1, sticky=tk.E)
    
    def refresh_contexts(self):
        """Refresh the context list."""
        try:
            print("DEBUG: Starting refresh_contexts()")
            self.status_var.set("Loading contexts...")
            
            # Clear existing items
            for item in self.context_tree.get_children():
                self.context_tree.delete(item)
            
            # Get contexts
            print(f"DEBUG: Config path: {self.config_manager.config_path}")
            print(f"DEBUG: Config file exists: {os.path.exists(self.config_manager.config_path)}")
            
            contexts = self.config_manager.get_contexts()
            current_context = self.config_manager.get_current_context()
            
            print(f"DEBUG: Found {len(contexts)} contexts")
            print(f"DEBUG: Current context: {current_context}")
            
            # Update current context display
            if current_context:
                self.current_context_var.set(current_context)
            else:
                self.current_context_var.set("None")
            
            # Populate treeview
            for context in contexts:
                name = context['name']
                cluster = context['context'].get('cluster', '')
                user = context['context'].get('user', '')
                namespace = context['context'].get('namespace', 'default')
                
                print(f"DEBUG: Adding context: {name}")
                
                # Mark current context with indicator
                if name == current_context:
                    self.context_tree.insert('', 'end', text='★',
                                           values=(name, cluster, user, namespace))
                else:
                    self.context_tree.insert('', 'end', text='',
                                           values=(name, cluster, user, namespace))
            
            self.status_var.set(f"Loaded {len(contexts)} contexts")
            print("DEBUG: refresh_contexts() completed successfully")
            
            # Force UI update
            self.root.update_idletasks()
            self.context_tree.update_idletasks()
            
        except Exception as e:
            print(f"DEBUG: Error in refresh_contexts(): {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load contexts:\n{str(e)}")
            self.status_var.set("Error loading contexts")
    
    def on_context_select(self, event):
        """Handle context selection."""
        selection = self.context_tree.selection()
        if selection:
            self.switch_btn.configure(state='normal')
            self.delete_btn.configure(state='normal')
        else:
            self.switch_btn.configure(state='disabled')
            self.delete_btn.configure(state='disabled')
    
    def on_context_double_click(self, event):
        """Handle double-click on context."""
        self.switch_context()
    
    def switch_context(self):
        """Switch to the selected context."""
        selection = self.context_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a context to switch to.")
            return
        
        try:
            item = selection[0]
            context_name = self.context_tree.item(item, 'values')[0]
            
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
        selection = self.context_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a context to delete.")
            return
        
        item = selection[0]
        context_name = self.context_tree.item(item, 'values')[0]
        
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
    
    # macOS specific fixes
    if os.uname().sysname == 'Darwin':
        root.tk.call('tk', 'scaling', 1.0)
    
    app = KubeContextGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Ensure window is visible
    root.deiconify()
    root.lift()
    root.focus_force()
    
    root.mainloop()


if __name__ == "__main__":
    main()