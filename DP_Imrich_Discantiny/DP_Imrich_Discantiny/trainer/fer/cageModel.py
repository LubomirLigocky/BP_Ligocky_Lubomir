import torchvision.models as models
import torch.nn as nn
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b4, EfficientNet_B4_Weights, EfficientNet
import torch.nn.functional as F
import torchvision
import re
import cv2

# Prebrate z https://github.com/wagner-niklas/CAGE_expression_inference/blob/main/inference_on_webcam.py

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)  # For Macbook, use mps

class CageModel():
    emotions = [
        "Neutral",
        "Happy",
        "Sad",
        "Suprise",
        "Fear",
        "Disgust",
        "Angry",
    ]

    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    MODEL = models.maxvit_t(weights="DEFAULT")
    block_channels = MODEL.classifier[3].in_features
    MODEL.classifier = nn.Sequential(
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.LayerNorm(block_channels),
        nn.Linear(block_channels, block_channels),
        nn.Tanh(),
        nn.Linear(
            block_channels, 9, bias=False
        ),  # Change the number of output classes, e.g. for AffectNet7 combined use 9 output neurons
    )
    MODEL.load_state_dict(
        torch.load(
            "fer/weights_cageNet/maxvit_t-bc5ab103.pth", map_location=torch.device(DEVICE)
        )
    )
    MODEL.eval()
    MODEL.to(DEVICE)

    test_transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )


    def detect_face(self, frame):
        faces = self.face_classifier.detectMultiScale(
            frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )

        return faces
    

    def recognizeEmotion(self, frame):
        faces = self.detect_face(frame)

        if len(faces) == 0:  # No faces detected
            print("No face detected!")
            return frame, []

        for x, y, w, h in faces:
            # Extract face ROI
            self.x = x
            self.y = y
            self.w = w
            self.h= h

            face_roi = frame[y : y + h, x : x + w]
        
            img = self.test_transform(face_roi)
            img = img.unsqueeze(0)  
        
            outputs = self.MODEL(img.to(DEVICE))
            outputs_cls = outputs[:, :7]  # First 7 values correspond to emotion classes

            # Apply softmax to get probabilities
            emotion_probs = F.softmax(outputs_cls, dim=1).detach().numpy()  # Converts logits to probabilities

            # Convert tensor to a list of probabilities
            emotions = emotion_probs.squeeze().tolist()
            
            self.valence = outputs[:, 7].squeeze().item()
            self.arousal = outputs[:, 8].squeeze().item()
        
            # self.createRectangleText(x, y, w, h, frame, f"{emotion} (V:{valence:.2f}, A:{arousal:.2f})")
            return frame, emotions  # Only process the first detected face

    def createRectangleText(self, color_image, text):
        size = 20
        start_x = max(self.x - size, 0)  # Ensure within image bounds
        start_y = max(self.y - size, 0)
        end_x = min(self.x + self.w + size, color_image.shape[1])
        end_y = min(self.y + self.h + size, color_image.shape[0])

        # Draw rectangle
        cv2.rectangle(color_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        # Draw text
        cv2.putText(color_image, text, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    def getDominantConfidence(self, emotions):

        cl = np.argmax(emotions[0])  # Get index of highest probability
        label = self.DICT_EMO[cl]  # Map index to emotion label
        confidence = str(round(float(emotions[0][cl]), 2)) 

        return label, confidence