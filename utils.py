import yaml
import cv2
import time
import os
import numpy as np

def load_config(config_path="config.yaml"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(ROOT_DIR, config_path)
    with open(full_path, "r") as f:
        return yaml.safe_load(f)

def get_class_labels(config):
    return config.get("classes", [])

def calculate_fps(start_time, frame_count):
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        return frame_count / elapsed_time
    return 0.0

def overlay_prediction(image, label, confidence, fps=None):
    # Overlays text on image (BGR format from cv2)
    h, w = image.shape[:2]
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2
    
    text_pred = f"{label}: {confidence*100:.1f}%"
    text_fps = f"FPS: {fps:.1f}" if fps is not None else ""
    
    # Drop shadow
    cv2.putText(image, text_pred, (20, 40), font, font_scale, (0, 0, 0), thickness + 1)
    cv2.putText(image, text_pred, (20, 40), font, font_scale, (0, 255, 0), thickness)
    
    if text_fps:
        cv2.putText(image, text_fps, (20, 80), font, font_scale, (0, 0, 0), thickness + 1)
        cv2.putText(image, text_fps, (20, 80), font, font_scale, (255, 255, 0), thickness)
        
    return image
