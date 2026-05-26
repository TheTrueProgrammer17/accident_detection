import tkinter as tk
from tkinter import scrolledtext

class DashboardUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Node 3 - Automated Authority Dashboard")
        self.root.geometry("900x800")
        self.root.configure(bg="#1e1e1e") # Dark control room theme
        
        # --- Top: Alert Banner ---
        self.banner_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.banner_frame.pack(fill=tk.X, pady=10)
        
        self.alert_label = tk.Label(
            self.banner_frame, 
            text="RoadSOS Automated Control Dashboard\nStatus: Monitoring incoming alerts...", 
            font=("Consolas", 20, "bold"), 
            fg="#00ff00", 
            bg="#1e1e1e",
            pady=15
        )
        self.alert_label.pack(fill=tk.X)

        # --- Middle: Details ---
        self.details_frame = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief=tk.FLAT)
        self.details_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.details_label = tk.Label(
            self.details_frame,
            text="Awaiting incident data...",
            font=("Consolas", 16),
            fg="white",
            bg="#2d2d2d",
            justify=tk.LEFT,
            pady=15,
            padx=15
        )
        self.details_label.pack(anchor="w")

        # --- Below: System Actions & Reasoning ---
        self.actions_frame = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief=tk.FLAT)
        self.actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.actions_title = tk.Label(
            self.actions_frame,
            text="SYSTEM ACTIONS:",
            font=("Consolas", 18, "bold"),
            fg="#00ffff",
            bg="#2d2d2d",
            padx=15,
            pady=10
        )
        self.actions_title.pack(anchor="w")
        
        self.actions_label = tk.Label(
            self.actions_frame,
            text="No actions dispatched.",
            font=("Consolas", 16, "bold"),
            fg="#ffcc00",
            bg="#2d2d2d",
            justify=tk.LEFT,
            padx=15,
            pady=5
        )
        self.actions_label.pack(anchor="w")
        
        self.reasoning_label = tk.Label(
            self.actions_frame,
            text="Decision Reason:\nN/A",
            font=("Consolas", 14, "italic"),
            fg="#aaaaaa",
            bg="#2d2d2d",
            justify=tk.LEFT,
            padx=15,
            pady=10
        )
        self.reasoning_label.pack(anchor="w")

        # --- Bottom: Logs ---
        self.logs_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.logs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        logs_title = tk.Label(
            self.logs_frame,
            text="EVENT LOG",
            font=("Consolas", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        logs_title.pack(anchor="w", pady=(0, 5))

        self.log_text = scrolledtext.ScrolledText(
            self.logs_frame, 
            font=("Consolas", 12), 
            bg="black", 
            fg="#00ff00", 
            state=tk.DISABLED,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """Add a message to the scrollable event log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_dashboard(self, alert_info, actions_text, reasoning_text):
        """Update the UI with alert details, actions, and reasoning."""
        # Update Banner to show red alert state
        self.alert_label.config(text="🚨 ACCIDENT DETECTED 🚨", fg="white", bg="#cc0000")
        self.banner_frame.config(bg="#cc0000")
        
        # Update Details
        details_str = (
            f"Location: {alert_info.get('location')}\n"
            f"Time: {alert_info.get('timestamp')}\n"
            f"Severity: {alert_info.get('severity', 'Unknown').upper()}"
        )
        self.details_label.config(text=details_str)
        
        # Update Actions & Reasoning
        self.actions_label.config(text=actions_text)
        self.reasoning_label.config(text=f"Decision Reason:\n{reasoning_text}")

    def reset_dashboard(self):
        """Reset the dashboard to monitoring state."""
        self.alert_label.config(text="RoadSOS Automated Control Dashboard\nStatus: Monitoring incoming alerts...", fg="#00ff00", bg="#1e1e1e")
        self.banner_frame.config(bg="#1e1e1e")
        self.details_label.config(text="Awaiting incident data...")
        self.actions_label.config(text="No actions dispatched.")
        self.reasoning_label.config(text="Decision Reason:\nN/A")
