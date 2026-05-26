"""
accident_node.py — Main entry point for Node 1 (Streetlight Camera)

This script orchestrates the full pipeline:
  1. Open the video source (accident.mp4).
  2. Run YOLOv8 detection on every frame (via detector.py).
  3. If an accident is detected, publish a JSON alert ONCE via MQTT.
  4. Display the annotated video in a live OpenCV window.
  5. Exit cleanly when the video ends or the user presses 'Q'.

Run:
    cd node1_detection
    python accident_node.py
"""

import sys
import cv2
from datetime import datetime, timezone

from config import (
    VIDEO_PATH,
    NODE_NAME,
    LOCATION,
    SEVERITY,
    WINDOW_NAME,
    FRAME_DELAY,
    COLLISION_FRAME_THRESHOLD,
    MOTION_SPIKE_THRESHOLD,
)
from detector import AccidentDetector
from mqtt_client import MQTTPublisher


def build_alert() -> dict:
    """Construct the standard JSON alert payload."""
    return {
        "node":      NODE_NAME,
        "event":     "accident_detected",
        "location":  LOCATION,
        "severity":  SEVERITY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    # ── 1. Initialise components ─────────────────────────────────
    print("=" * 60)
    print("  RoadSOS — Node 1: Smart Streetlight Accident Detector")
    print("=" * 60)

    detector  = AccidentDetector()
    publisher = MQTTPublisher()
    publisher.connect()

    # ── 2. Open video source ─────────────────────────────────────
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {VIDEO_PATH}")
        sys.exit(1)

    print(f"[VIDEO] Opened: {VIDEO_PATH}")
    print(f"[VIDEO] Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}×"
          f"{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"[VIDEO] FPS: {cap.get(cv2.CAP_PROP_FPS):.1f}")
    print("-" * 60)
    print("Press 'Q' to quit.\n")

    alert_sent = False               # Ensure we only alert ONCE per run.
    accident_frame_counter = 0       # Consecutive frames with collision signal.
    final_confidence = 0.0           # Store confidence score when collision detected

    cv2.namedWindow("RoadSOS Node 1 Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("RoadSOS Node 1 Detection", 1280, 720)
    cv2.setWindowTitle("RoadSOS Node 1 Detection", "RoadSOS Node 1 Monitoring Traffic")

    # ── 3. Frame-by-frame processing loop ────────────────────────
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\n[VIDEO] End of video reached.")
                break

            frame = cv2.resize(frame, (1280, 720))

            # Run YOLOv8 detection + motion diffing.
            annotated, has_vehicles, motion_intensity = detector.process_frame(frame)

            motion_ratio = motion_intensity / MOTION_SPIKE_THRESHOLD
            collision_confidence = min(1.0, motion_ratio)

            # ── Stabilised collision detection ───────────────────
            collision_detected = False
            if not alert_sent:
                if detector.is_collision(has_vehicles, motion_intensity):
                    accident_frame_counter += 1
                else:
                    accident_frame_counter = 0

                if accident_frame_counter >= COLLISION_FRAME_THRESHOLD:
                    collision_detected = True

                if collision_detected and alert_sent == False:
                    alert = build_alert()
                    print("\nCollision detected:")
                    print(f"Confidence: {collision_confidence:.2f}")
                    print("Reason: sudden motion spike detected across multiple frames")
                    print("🚨  Publishing alert …")
                    publisher.publish_alert(alert)
                    cv2.setWindowTitle("RoadSOS Node 1 Detection",
                                      "RoadSOS Node 1 Collision Detected")
                    final_confidence = collision_confidence
                    alert_sent = True

            # Overlay a status bar at the top of the frame.
            if alert_sent:
                cv2.putText(
                    annotated, f"Collision detected (confidence: {final_confidence:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255), 2,
                )
                cv2.putText(
                    annotated, "Collision detected (motion spike threshold exceeded)",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255), 2,
                )
            else:
                cv2.putText(
                    annotated, "Node 1 | Monitoring traffic...",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2,
                )

            # Show the live detection window.
            cv2.imshow("RoadSOS Node 1 Detection", annotated)

            # 'Q' to quit.
            if cv2.waitKey(FRAME_DELAY) & 0xFF == ord("q"):
                print("\n[USER] Quit requested.")
                break

    except KeyboardInterrupt:
        print("\n[USER] Interrupted (Ctrl+C).")

    # ── 4. Cleanup ───────────────────────────────────────────────
    finally:
        cap.release()
        cv2.destroyAllWindows()
        publisher.disconnect()
        print("[NODE 1] Shutdown complete.")


if __name__ == "__main__":
    main()
