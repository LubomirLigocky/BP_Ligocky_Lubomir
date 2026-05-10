from typing import List, Dict
from pathlib import Path
import argparse

import numpy as np
import torch
from torch import nn
from skimage import io
from face_alignment.detection.sfd.sfd_detector import SFDDetector
from fer.weights_emonet.emonet import EmoNet

import cv2

import sys
sys.path.append('/weights_emonet')

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)  # For Macbook, use mps
print(DEVICE)

class EmonetModel:
    torch.backends.cudnn.benchmark = True

    
    # Parameters of the experiments
    n_expression = 8
    device = "cuda:0"
    image_size = 256
    emotion_classes = {
        0: "Neutral",
        1: "Happy",
        2: "Sad",
        3: "Surprise",
        4: "Fear",
        5: "Disgust",
        6: "Anger",
        7: "Contempt",
    }

    state_dict_path = Path(__file__).parent.joinpath(
        "fer/weights_emonet", f"emonet_{n_expression}.pth"
    )

    state_dict = torch.load("fer/weights_emonet/emonet_8.pth", map_location=DEVICE)
    state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    net = EmoNet(n_expression=n_expression).to(DEVICE)
    net.load_state_dict(state_dict, strict=False)
    net.eval()

    sfd_detector = SFDDetector("cuda:0")

    def detect_face(self, frame):
        with torch.no_grad():
            # Face detector requires BGR frame
            detected_faces = self.sfd_detector.detect_from_image(frame[:, :, ::-1])

            return detected_faces

    def recognizeEmotion(self, frame):
        frame_copy = frame.copy()
        faces = self.detect_face(frame)
      

        if len(faces) == 0:  # No faces detected
            print("No face detected!")
            return frame, []

        for face in faces:
            # Extract face ROI
            bbox = np.array(face).astype(np.int32)
            x, y, w, h = bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Extract face crop using bbox
            face_crop = frame[y : y + h, x : x + w, :]

            # Store bounding box values
            self.x, self.y, self.w, self.h = x, y, w, h

            # Resize image to (256,256)
            image_size = 256  # Define image size
            image_rgb = cv2.resize(face_crop, (image_size, image_size))

            # Load image into a tensor: convert to RGB, and put the tensor in the [0;1] range
            image_tensor = torch.Tensor(image_rgb).permute(2, 0, 1).to(self.device) / 255.0

            # Run emotion model inference
            with torch.no_grad():
                output = self.net(image_tensor.unsqueeze(0))
                emotions = nn.functional.softmax(output["expression"], dim=1).cpu().detach().numpy()
               
            return frame_copy, emotions
        
    
    def createRectangleText(self, color_image, text):
        # print(color_image.data)
        size = 20
        start_x = max(self.x - size, 0)  # Ensure within image bounds
        start_y = max(self.y - size, 0)
        end_x = min(self.x + self.w + size, color_image.shape[1])
        end_y = min(self.y + self.h + size, color_image.shape[0])

        
        cv2.rectangle(color_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

     
        cv2.putText(color_image, text, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        return color_image

    def getDominantConfidence(self, emotions):

        predicted_indices = emotions.argmax(axis=1)  # Index of highest probability
        confidence_scores = emotions.max(axis=1)
        
        emotion_label = self.emotion_classes[predicted_indices[0]]  # Emotion label for the first face
        emotion_confidence = confidence_scores[0]
        return emotion_label,  str(round(float(emotion_confidence), 2))