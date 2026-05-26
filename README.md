# SadakSuraksha Grid – AI Accident Detection Prototype

SadakSuraksha Grid is a software-based prototype that demonstrates how AI-powered smart infrastructure can automatically detect road accidents and coordinate emergency responses using distributed communication nodes and computer vision.

This project simulates a network of smart streetlights and edge nodes that process video feeds, detect accidents in real-time, and relay alerts using the MQTT protocol.

## 🌟 Features

- **Real-Time AI Detection**: Uses YOLOv8 and OpenCV to analyze video frames and detect accidents.
- **Distributed Architecture**: Implements 3 separate MQTT nodes to simulate a distributed IoT network (Detection, Relay, and Dashboard).
- **Fast Alert System**: Instantly propagates critical accident events across the network for rapid emergency response.
- **Hardware-Ready Vision**: While currently software-based, the architecture is designed to map directly onto physical edge devices (like ESP32/Jetson Nano).

## 📁 Project Structure

```
roadsos/
│
├── node1_detection/      # Detection node (Runs AI models on video feeds)
│   └── accident_node.py
│
├── node2_relay/          # Communication/relay node (Simulates mesh routing)
│   └── relay_node.py     # (or relevant script)
│
├── node3_dashboard/      # Alert/dashboard node (Receives signals and displays alerts)
│   └── dashboard_node.py # (or relevant script)
│
├── accident.mp4          # Sample accident video 1
├── accident2.mp4         # Sample accident video 2
├── yolov8n.pt            # Pre-trained YOLOv8 weights
└── SadakSuraksha_Grid_Technical_Documentation.docx  # Full Technical Documentation
```

## 🛠️ Prerequisites

Before you begin, ensure you have met the following requirements:
- **Python 3.8+** installed on your machine.
- An **MQTT Broker** running locally or remotely (e.g., [Eclipse Mosquitto](https://mosquitto.org/)).

## ⚙️ Installation & Setup

1. **Activate the Virtual Environment**
   If you haven't already, activate the provided virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**
   Make sure you have the required Python packages installed (like OpenCV, Ultralytics YOLO, Paho-MQTT):
   ```bash
   pip install opencv-python ultralytics paho-mqtt
   ```

3. **Start the MQTT Broker**
   Ensure your local MQTT broker (e.g., Mosquitto) is running.
   ```bash
   # Example for Mosquitto on Linux
   sudo systemctl start mosquitto
   ```

## 🚀 How to Run the Prototype

To see the full distributed system in action, you need to start the nodes. It is recommended to run each node in a separate terminal window so you can observe the real-time communication.

### Terminal 1: Start the Dashboard Node (Node 3)
This node will listen for alerts and display warnings when an accident is detected.
```bash
source venv/bin/activate
cd node3_dashboard
python dashboard_node.py  # (Adjust filename based on your exact script name)
```

### Terminal 2: Start the Relay Node (Node 2)
This node simulates a relay in the mesh network, passing messages from the detection node to the dashboard.
```bash
source venv/bin/activate
cd node2_relay
python relay_node.py      # (Adjust filename based on your exact script name)
```

### Terminal 3: Start the Detection Node (Node 1)
This node will process the video feed (`accident.mp4` or `accident2.mp4`) using YOLO. When an accident is detected, it publishes an alert.
```bash
source venv/bin/activate
cd node1_detection
python accident_node.py
```

*Note: Ensure the paths to the video files (`../accident.mp4`) and model weights (`../yolov8n.pt`) inside `accident_node.py` correctly point to the files in the root directory.*

## 📖 Documentation

For a deep dive into the system workflow, technical architecture, feasibility analysis, and future hardware vision, please refer to the generated technical documentation:
**`SadakSuraksha_Grid_Technical_Documentation.docx`**

### Sample: Alert Generation Logic
Here is a snippet from the detection node (`node1_detection/accident_node.py`) demonstrating how the payload is built when a collision is detected:

```python
def build_alert() -> dict:
    """Construct the standard JSON alert payload."""
    return {
        "node":      NODE_NAME,
        "event":     "accident_detected",
        "location":  LOCATION,
        "severity":  SEVERITY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
```

## 🔮 Future Scope

- Integration with real-time RTSP CCTV streams.
- Deployment onto physical ESP32-S3 and Edge AI microcontrollers.
- Integration with local emergency dispatch APIs (e.g., ArogyaVault).

---
*Built for Hackathon Submission*
