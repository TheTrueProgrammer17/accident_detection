"""
detector.py — YOLOv8 + Frame-diff motion spike collision detection for Node 1

Responsibilities
-----------------
1. Load a YOLOv8 model (ultralytics).
2. Run inference on a single video frame to detect vehicles.
3. Draw bounding boxes + labels on the frame.
4. Compute frame-to-frame pixel difference (absdiff).
5. Calculate total motion intensity.
6. Flag a collision if motion intensity spikes AND vehicles are present.

All detection logic is isolated here so that accident_node.py
stays clean and focused on orchestration.
"""

import cv2
import numpy as np
from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    YOLO_CONFIDENCE,
    TARGET_CLASSES,
    VEHICLE_CLASSES,
    MOTION_SPIKE_THRESHOLD,
)


class AccidentDetector:
    """YOLOv8 inference + frame-difference motion spike detection."""

    # Colour palette for bounding boxes (BGR).
    _COLOURS = {
        "car":        (0, 255, 0),
        "bicycle":    (255, 200, 0),
        "motorcycle": (255, 200, 0),
        "motorbike":  (255, 200, 0),
        "bus":        (0, 200, 255),
        "truck":      (0, 165, 255),
        "person":     (0, 0, 255),
    }
    _DEFAULT_COLOUR = (200, 200, 200)

    def __init__(self):
        print(f"[DETECTOR] Loading YOLO model: {YOLO_MODEL} …")
        self.model = YOLO(YOLO_MODEL)
        print("[DETECTOR] Model loaded ✔")

        # Cache for the previous frame (grayscale)
        self.prev_gray = None

    # ── Core inference ───────────────────────────────────────────

    def process_frame(self, frame):
        """
        Run YOLOv8 on a single BGR frame and compute motion intensity.

        Returns
        -------
        annotated_frame : numpy.ndarray
            The frame with bounding boxes drawn.
        has_vehicles : bool
            Whether at least one vehicle was detected in this frame.
        motion_intensity : float
            Sum of pixel differences between this frame and the last.
        """
        # Run inference (verbose=False suppresses per-frame logs).
        results = self.model(frame, conf=YOLO_CONFIDENCE, verbose=False)

        has_vehicles = False

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = self.model.names[cls_id]

                # Only draw / track classes we care about.
                if class_name not in TARGET_CLASSES:
                    continue

                if class_name in VEHICLE_CLASSES:
                    has_vehicles = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])

                # Draw bounding box + label.
                colour = self._COLOURS.get(class_name, self._DEFAULT_COLOUR)
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(
                    frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2,
                )

        # ── Frame differencing ───────────────────────────────────
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply slight blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        motion_intensity = 0.0

        if self.prev_gray is not None:
            # Compute absolute difference
            diff = cv2.absdiff(self.prev_gray, gray)
            
            # Threshold to get clear motion pixels
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            
            # Sum up pixel differences
            motion_intensity = np.sum(thresh)

        self.prev_gray = gray

        return frame, has_vehicles, motion_intensity

    # ── Collision rule (motion spike) ────────────────────────────

    def is_collision(self, has_vehicles: bool, motion_intensity: float) -> bool:
        """
        Detect a likely collision if vehicles are present AND there's
        a massive sudden motion spike (e.g. dust cloud / scene shake).

        Parameters
        ----------
        has_vehicles : bool
            True if 1+ vehicles detected.
        motion_intensity : float
            Calculated motion intensity for the current frame.

        Returns
        -------
        bool
        """
        return has_vehicles and motion_intensity > MOTION_SPIKE_THRESHOLD
