import tkinter as tk

class NodeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Node 2 - Streetlight Relay")
        # Full window size
        self.root.geometry("1024x768")
        
        # State variable to prevent repeated/overlapping flashing
        self.alert_active = False
        self.flash_state = False
        
        # Setup initial UI state
        self.bg_color = "dark green"
        self.root.configure(bg=self.bg_color)
        
        # Large, bold, centered text for the main label
        self.main_label = tk.Label(
            self.root, 
            text="Monitoring Traffic", 
            font=("Helvetica", 48, "bold"), 
            fg="white", 
            bg=self.bg_color
        )
        self.main_label.pack(expand=True)

        self.sub_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 32, "bold"),
            fg="white",
            bg=self.bg_color
        )
        self.sub_label.pack(expand=True)

    def trigger_alert(self, location, timestamp):
        # Alert handling: If alert already active, do not restart flashing again
        if self.alert_active:
            return
            
        self.alert_active = True
        
        # Update text for the alert
        self.main_label.config(text="⚠ ACCIDENT AHEAD ⚠")
        self.sub_label.config(text=f"Location: {location}\nTime: {timestamp}")
        
        # Start the GUI flashing logic
        self.flash_warning()

    def flash_warning(self):
        # GUI flashing logic
        if not self.alert_active:
            return
            
        # Toggle background color between RED and BLACK
        if self.flash_state:
            current_bg = "black"
        else:
            current_bg = "red"
            
        self.flash_state = not self.flash_state
        
        self.root.configure(bg=current_bg)
        self.main_label.configure(bg=current_bg)
        self.sub_label.configure(bg=current_bg)
        
        # Use tkinter .after() loop for flashing every 500ms
        self.root.after(500, self.flash_warning)

    def reset_alert(self):
        # Reset to normal state
        self.alert_active = False
        self.bg_color = "dark green"
        self.root.configure(bg=self.bg_color)
        self.main_label.config(text="Monitoring Traffic", bg=self.bg_color)
        self.sub_label.config(text="", bg=self.bg_color)
