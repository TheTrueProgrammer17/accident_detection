"""
mqtt_client.py — MQTT publisher for Node 1

Encapsulates all MQTT logic (connect / publish / disconnect) so that
the rest of the application never touches paho-mqtt directly.
"""

import json
import paho.mqtt.client as mqtt

from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_CLIENT_ID


class MQTTPublisher:
    """Lightweight wrapper around paho-mqtt for publishing JSON alerts."""

    def __init__(self):
        # Create the MQTT client with the node's unique ID.
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)

        # Optional: register callbacks for debugging.
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

        self._connected = False

    # ── Callbacks ────────────────────────────────────────────────

    def _on_connect(self, client, userdata, flags, rc):
        """Called when the broker acknowledges our connection."""
        if rc == 0:
            self._connected = True
            print(f"[MQTT] Connected to broker at {MQTT_BROKER}:{MQTT_PORT}")
        else:
            print(f"[MQTT] Connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Called when we disconnect (cleanly or otherwise)."""
        self._connected = False
        print("[MQTT] Disconnected from broker")

    # ── Public API ───────────────────────────────────────────────

    def connect(self):
        """Establish a connection to the MQTT broker."""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            # Start a background thread so callbacks fire.
            self.client.loop_start()
        except ConnectionRefusedError:
            print("[MQTT] ⚠  Broker not reachable — alerts will be printed "
                  "locally but NOT published.")

    def publish_alert(self, alert: dict) -> None:
        """
        Publish a JSON-encoded alert dict to the configured topic.

        Parameters
        ----------
        alert : dict
            Must contain keys: node, event, location, severity, timestamp.
        """
        payload = json.dumps(alert, indent=2)

        if self._connected:
            result = self.client.publish(MQTT_TOPIC, payload, qos=1)
            result.wait_for_publish()
            print(f"[MQTT] Alert published to '{MQTT_TOPIC}'")
        else:
            print("[MQTT] Broker unavailable — alert NOT published")

        # Always print the payload to the terminal for visibility.
        print(f"[ALERT] {payload}")

    def disconnect(self):
        """Cleanly shut down the MQTT connection."""
        self.client.loop_stop()
        self.client.disconnect()
