
import cv2
from deepface import DeepFace
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"

class DeepFaceModel():
    
    def __init__(self):
        pass

    def detectFaces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(40, 40)
        )

        return faces

    def recognizeEmotion(self, frame):
        faces = self.detectFaces(frame)

        for (x, y, w, h) in faces:

            roi_color = frame[y:y + h, x:x + w]
            
            a = DeepFace.analyze(img_path = roi_color, actions = ['emotion'], enforce_detection=False, detector_backend="opencv")
            break
        
        return a
    
    def getDominantConfidence(self, em):
        dominant_emo = em[0]['dominant_emotion']
            
        rounded_confidence = round(em[0]["emotion"][dominant_emo], 2)

        return (dominant_emo, rounded_confidence)

     
    
    