<<<<<<< HEAD
# SignSight Vision – Traffic Sign Recognition System

🎯 **Project Goal**: A lightweight autonomous perception prototype optimized for CPU inference on low-end PCs.

This system detects and classifies traffic signs using transfer learning with a pretrained MobileNetV2 architecture. It focuses on a reduced subset of the German Traffic Sign Recognition Benchmark (GTSRB) to remain lightweight and fully playable in real-time without GPU acceleration.

## 🧠 Technical Approach

- **Model**: MobileNetV2 (pretrained on ImageNet), fine-tuned final layers.
- **Dataset**: Reduced GTSRB subset (12 selected high-impact classes).
- **Optimization**: Resolution scaled to 96x96, `model.eval()` used during inference, and limited batch sizes for training.
- **Backend API**: FastAPI generating MJPEG streams for webcam and JSON endpoints for image uploads.
- **Frontend**: Modern, interactive UI built with pure HTML/CSS/JS, featuring glassmorphism and smooth animations.

## 🚀 Features

- **Upload Mode**: Drag and drop images for high-accuracy predictions.
- **Live Webcam Mode**: Real-time traffic sign classification on a live video feed.
- **Lightweight**: Optimized to run smoothly on just 8GB RAM, CPU only.

## ⚙️ Installation & Execution

1. **Install Requirements**
```bash
pip install -r requirements.txt
```

2. **(Optional) Train the model**
```bash
python train.py
```
*Note: A dummy dataset will be generated during training if the GTSRB dataset is unavailable.*

3. **Run the Application**
```bash
python backend/main.py
```

4. **Access the App**
Open your browser and navigate to `http://localhost:8000`.

## 📄 Resume Description
*Developed a CPU-optimized Traffic Sign Recognition System using transfer learning with MobileNetV2 on a reduced GTSRB dataset, implementing real-time classification with a modern interactive web interface to simulate autonomous perception modules.*
=======
# SignSight-Vision
SignSight Vision – Traffic Sign Recognition System is a lightweight autonomous perception prototype designed to detect and classify traffic signs using deep learning and computer vision. The system simulates the traffic sign recognition module used in modern Advanced Driver Assistance Systems (ADAS) and autonomous vehicles.
>>>>>>> 70a54b7f7d25add59b5ee9398880dd632e646249
