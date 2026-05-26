import paho.mqtt.client as mqtt
import json
import config

class MQTTClient:
    def __init__(self, on_message_callback):
        self.client = mqtt.Client(client_id="node2_relay")
        self.on_message_callback = on_message_callback
        
        # Assign callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # Subscribe to the alerts topic to receive accident notifications
            # This is where Node 2 listens for incoming alerts from Node 1
            self.client.subscribe(config.SUBSCRIBE_TOPIC)
        else:
            print(f"Failed to connect to MQTT broker with return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            # Parse the incoming JSON message
            payload = json.loads(msg.payload.decode("utf-8"))
            # Trigger the callback function passed from relay_node.py
            self.on_message_callback(payload)
        except json.JSONDecodeError:
            print("Received invalid JSON message")
        except Exception as e:
            print(f"Error handling message: {e}")

    def publish_relay(self, payload):
        # Forward the same message to the relay topic
        self.client.publish(config.PUBLISH_TOPIC, json.dumps(payload))

    def start(self):
        # Connect to the MQTT broker
        self.client.connect(config.BROKER_IP, config.PORT, 60)
        # Start the network loop in a background thread
        self.client.loop_start()

    def stop(self):
        # Stop the network loop and disconnect
        self.client.loop_stop()
        self.client.disconnect()
