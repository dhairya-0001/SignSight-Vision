import torch
import torch.nn as nn
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

class SignClassifier(nn.Module):
    def __init__(self, num_classes=12):
        super(SignClassifier, self).__init__()
        # Load pretrained MobileNetV2
        self.model = mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V1)
        
        # Freeze all layers first
        for param in self.model.parameters():
            param.requires_grad = False
            
        # Unfreeze the last few layers
        for param in self.model.features[17:].parameters():
            param.requires_grad = True
            
        # Replace the final classifier
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=False),
            nn.Linear(in_features, num_classes)
        )
        
    def forward(self, x):
        return self.model(x)

def load_model(weights_path, num_classes):
    model = SignClassifier(num_classes=num_classes)
    try:
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
        print(f"Model weights loaded from {weights_path}")
    except Exception as e:
        print(f"Could not load weights from {weights_path}, starting fresh. Warning: {e}")
    
    model.eval() # Force inference mode (no gradients, batchnorm frozen)
    return model
