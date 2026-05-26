# config.py
# Configuration for Node 3 (Automated Authority Dashboard)

# MQTT Broker settings
BROKER_IP = "localhost"
PORT = 1883

# Subscribe to both direct alerts and relayed messages
SUBSCRIBE_TOPICS = [
    ("roadsos/alerts", 0),
    ("roadsos/relay", 0)
]
