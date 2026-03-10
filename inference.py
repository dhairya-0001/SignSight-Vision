import os
import torch
import torchvision.transforms as transforms
from PIL import Image
import time
import numpy as np
from model import load_model
from utils import load_config, get_class_labels

class SignPredictor:
    def __init__(self, config_path="config.yaml", model_path="models/sign_classifier.pth"):
        self.config = load_config(config_path)
        self.num_classes = self.config["num_classes"]
        self.image_size = self.config["image_size"]
        self.classes = get_class_labels(self.config)
        self.threshold = self.config["confidence_threshold"]
        
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        full_model_path = os.path.join(ROOT_DIR, model_path)
        
        self.model = load_model(full_model_path, self.num_classes)
        
        self.transform = transforms.Compose([
            transforms.Resize((self.image_size, self.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image):
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
            
        start_time = time.time()
        
        input_tensor = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            
        confidence, predicted_idx = torch.max(probabilities, 0)
        confidence = confidence.item()
        
        fps = 1.0 / (time.time() - start_time)
        
        if confidence >= self.threshold:
            try:
                label = self.classes[predicted_idx.item()]
            except IndexError:
                label = "Unknown"
        else:
            label = "Unknown"
            
        return {
            "label": label,
            "confidence": confidence,
            "fps": fps
        }
