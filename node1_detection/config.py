"""
config.py — Configuration for Node 1 (Streetlight Accident Detection)

Centralises every tuneable parameter so that no magic values
are scattered across the codebase.  Edit this file to change
the MQTT broker, detection thresholds, video source, etc.
"""

import os

# ─── Video source ────────────────────────────────────────────────
# Path is resolved relative to the *project root* (one level up).
VIDEO_PATH = os.path.join(os.path.dirname(__file__), "..", "accident.mp4")

# ─── YOLO model ──────────────────────────────────────────────────
YOLO_MODEL = "yolov8n.pt"          # Nano model — fast, good for demos
YOLO_CONFIDENCE = 0.45             # Minimum confidence to keep a detection

# ─── Object classes of interest ──────────────────────────────────
# These are COCO class names that YOLOv8 recognises out of the box.
TARGET_CLASSES = {"car", "bicycle", "bus", "truck", "person",
                  "motorcycle", "motorbike"}

# ─── Collision detection (motion-based) ──────────────────────────
# Instead of checking bounding-box overlap (unreliable for front-view
# CCTV), we track each vehicle's center across frames and flag a
# collision when a vehicle that WAS moving suddenly stops.
VEHICLE_CLASSES = {"car", "bicycle", "bus", "truck", "motorcycle", "motorbike"}

# Motion spike detection (frame-differencing)
# Uses OpenCV absdiff to detect sudden large scene changes (e.g. dust clouds)
MOTION_SPIKE_THRESHOLD     = 2000000   # sum of pixel differences
COLLISION_FRAME_THRESHOLD  = 3         # Consecutive suspicious frames before alert

# ─── MQTT broker ─────────────────────────────────────────────────
MQTT_BROKER   = "localhost"
MQTT_PORT     = 1883
MQTT_TOPIC    = "roadsos/alerts"
MQTT_CLIENT_ID = "streetlight_node_01"

# ─── Alert metadata ─────────────────────────────────────────────
NODE_NAME     = "streetlight_node_01"
LOCATION      = "Demo Junction"
SEVERITY      = "medium"

# ─── Display ─────────────────────────────────────────────────────
WINDOW_NAME   = "RoadSOS — Node 1 Detection"
FRAME_DELAY   = 1   # ms — OpenCV waitKey delay (1 = max speed)
