import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import torch.optim as optim
from model import load_model
from utils import load_config

class DummyDataset(Dataset):
    def __init__(self, length, transform=None):
        self.length = length
        self.transform = transform
        
    def __len__(self):
        return self.length
        
    def __getitem__(self, idx):
        from PIL import Image
        import numpy as np
        img = Image.fromarray(np.random.randint(0, 255, (96, 96, 3), dtype=np.uint8))
        label = np.random.randint(0, 12)
        if self.transform:
            img = self.transform(img)
        return img, label

def train():
    config = load_config()
    image_size = config["image_size"]
    batch_size = config["batch_size"]
    learning_rate = config["learning_rate"]
    epochs = config["epochs"]
    num_classes = config["num_classes"]
    
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(ROOT_DIR, "dataset", "gtsrb_subset")
    
    try:
        train_dataset = datasets.ImageFolder(dataset_path, transform=transform)
        print(f"Loaded dataset from {dataset_path}")
    except Exception as e:
        print(f"Failed to load dataset: {e}. Using dummy dataset for testing.")
        train_dataset = DummyDataset(100, transform=transform)
        
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    model_path = os.path.join(ROOT_DIR, "models", "sign_classifier.pth")
    model = load_model(model_path, num_classes=num_classes)
    model.train()
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if i % 10 == 9:
                print(f"[Epoch {epoch + 1}, Batch {i + 1}] loss: {running_loss / 10:.3f}")
                running_loss = 0.0
                
    print("Finished Training")
    models_dir = os.path.join(ROOT_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)
    torch.save(model.state_dict(), model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    train()
