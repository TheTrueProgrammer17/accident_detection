import tkinter as tk
from mqtt_client import MQTTClient
from ui import NodeUI

class RelayNode:
    def __init__(self):
        # Initialize Tkinter root
        self.root = tk.Tk()
        self.ui = NodeUI(self.root)
        
        # Initialize MQTT client with callback for message handling
        self.mqtt_client = MQTTClient(self.handle_alert)

    def handle_alert(self, payload):
        # Alert handling: parse JSON message fields
        location = payload.get("location", "Unknown")
        timestamp = payload.get("timestamp", "Unknown")

        # Print terminal output for received alert
        print("\nALERT RECEIVED")
        print(f"Location: {location}")
        print(f"Time: {timestamp}")
        
        # Activate warning system in GUI
        # Use root.after to safely update the tkinter UI from the MQTT thread
        self.root.after(0, self.ui.trigger_alert, location, timestamp)

        # Forward alert: Republish SAME message to relay topic
        print("Forwarding alert to network...")
        self.mqtt_client.publish_relay(payload)

    def start(self):
        # Print starting messages
        print("Node 2 (Streetlight Relay) Started")
        print("Status: Monitoring network...")
        
        # Connect and start the MQTT client
        self.mqtt_client.start()
        
        # Start tkinter main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.mqtt_client.stop()

if __name__ == "__main__":
    node = RelayNode()
    node.start()
