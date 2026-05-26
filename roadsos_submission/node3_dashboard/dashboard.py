import tkinter as tk
from datetime import datetime
from mqtt_client import MQTTClient
from ui import DashboardUI

class AutomatedDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = DashboardUI(self.root)
        self.mqtt_client = MQTTClient(self.handle_message)
        
        # Track recent alert times by location to prevent duplicate processing
        self.processed_alerts = {}

    def analyze_and_dispatch(self, severity):
        """Determine automated actions based on severity."""
        severity = str(severity).lower()
        actions = []
        reason = ""
        
        if severity == "low":
            actions.append("✔ Police Notified")
            reason = "Low severity collision detected, minor property damage expected."
        elif severity == "medium":
            actions.append("✔ Ambulance Dispatched")
            actions.append("✔ Police Notified")
            reason = "Medium severity collision detected, potential injuries requiring medical assistance."
        elif severity in ["high", "critical", "severe"]:
            actions.append("✔ Ambulance Dispatched")
            actions.append("✔ Police Notified")
            actions.append("✔ Fire Brigade Alerted")
            reason = "High severity collision detected, possible severe injuries and fire risk."
        else:
            actions.append("✔ Police Notified")
            reason = f"Unknown severity ({severity}) detected, dispatching standard police response."
            
        return "\n".join(actions), reason

    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def schedule_log(self, message, delay_ms):
        """Helper to schedule log messages so they simulate sequential processing."""
        self.root.after(delay_ms, self.ui.log_message, message)

    def handle_message(self, topic, payload):
        location = payload.get("location", "Unknown")
        severity = payload.get("severity", "Unknown")
        timestamp = payload.get("timestamp", "Unknown")

        # Deduplication logic
        # Prevent processing the same exact alert if received via both topics
        alert_key = f"{location}_{timestamp}"
        if alert_key in self.processed_alerts:
            return
            
        self.processed_alerts[alert_key] = True

        # Analyze severity and determine dispatch logic
        actions_text, reasoning_text = self.analyze_and_dispatch(severity)
        
        alert_info = {
            "location": location,
            "timestamp": timestamp,
            "severity": severity
        }
        
        # Schedule timeline logs
        t_received = self.get_current_time()
        self.schedule_log(f"[{t_received}] Alert received (Topic: {topic})", 0)
        self.schedule_log(f"[{t_received}] Severity analyzed: {severity.upper()}", 500)
        self.schedule_log(f"[{t_received}] Services dispatched automatically", 1000)

        # Update the UI on the main thread after the "processing" delay
        self.root.after(1000, self.ui.update_dashboard, alert_info, actions_text, reasoning_text)

    def start(self):
        # Connect and start MQTT
        self.mqtt_client.start()
        
        # Log initialization
        self.ui.log_message(f"[{self.get_current_time()}] System initialized. Monitoring alerts and relay networks...")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.mqtt_client.stop()

if __name__ == "__main__":
    app = AutomatedDashboard()
    app.start()
