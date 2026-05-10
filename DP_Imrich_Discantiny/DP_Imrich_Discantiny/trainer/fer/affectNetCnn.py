import cv2
import mediapipe as mp #face detector
import math
import numpy as np
import time

# torch
import torch
from PIL import Image
from torchvision import transforms

class AffectNetModel():

    DICT_EMO = {0: 'Neutral', 1: 'Happiness', 2: 'Sadness', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger'}
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.25, min_tracking_confidence=0.45)

    name = '0_66_49_wo_gl'

    # torch
    pth_model = torch.jit.load('fer/weights_affectNet/torchscript_model_{0}.pth'.format(name)).to('cuda')
    pth_model.eval()
    
    def __init__(self):
        pass

    def createRectangleText(self, frame, text):

        start_x = self.startX 
        start_y = self.startY 
        end_x =  self.endX 
        end_y = self.endY 
        
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.putText(frame, text, ( start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 300, 12), 2)

        return frame

    def recognizeEmotion(self, frame):
       
        results = self.detectFaces(frame)

        if results == None:
            # print("No Face")
            return frame, []
        
        height, width, _ = frame.shape
        
        for fl in results.multi_face_landmarks:
            self.startX, self.startY, self.endX, self.endY  = self.get_box(fl, width, height)
            cur_face = frame[self.startY:self.endY, self.startX: self.endX]
            
            # torch
            cur_face = self.pth_processing(Image.fromarray(cur_face))
            output = torch.nn.functional.softmax(self.pth_model(cur_face), dim=1).cpu().detach().numpy()

            # cl = np.argmax(output)
            # label = self.DICT_EMO[cl]
            # frame = self.createRectangleText(frame, label)
            return frame, output
        
    
    def detectFaces(self, frame):
        frame_copy = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        frame_copy.flags.writeable = True
        
        results = self.face_mesh.process(frame_copy)

        if results.multi_face_landmarks:
            return results
        
        return None
        
    def getDominantConfidence(self, emotions):
        cl = np.argmax(emotions)
        label = self.DICT_EMO[cl] # Label

        # Get confidence score (probability value)
        confidence = str(round(float(emotions[0][cl]), 2))

        return (label, confidence)
    
   
    def get_box(self, fl, w, h):
        idx_to_coors = {}
        for idx, landmark in enumerate(fl.landmark):
            landmark_px = self.norm_coordinates(landmark.x, landmark.y, w, h)

            if landmark_px:
                idx_to_coors[idx] = landmark_px

        x_min = np.min(np.asarray(list(idx_to_coors.values()))[:,0])
        y_min = np.min(np.asarray(list(idx_to_coors.values()))[:,1])
        endX = np.max(np.asarray(list(idx_to_coors.values()))[:,0])
        endY = np.max(np.asarray(list(idx_to_coors.values()))[:,1])

        (startX, startY) = (max(0, x_min), max(0, y_min))
        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
        
        return startX, startY, endX, endY
    
    def pth_processing(self, fp):
        class PreprocessInput(torch.nn.Module):
            def init(self):
                super(PreprocessInput, self).init()

            def forward(self, x):
                x = x.to(torch.float32)
                x = torch.flip(x, dims=(0,))
                x[0, :, :] -= 91.4953
                x[1, :, :] -= 103.8827
                x[2, :, :] -= 131.0912
                return x

        def get_img_torch(img):
            
            ttransform = transforms.Compose([
                transforms.PILToTensor(),
                PreprocessInput()
            ])
            img = img.resize((224, 224), Image.Resampling.NEAREST)
            img = ttransform(img)
            img = torch.unsqueeze(img, 0).to('cuda')
            return img
        return get_img_torch(fp)

    def norm_coordinates(self, normalized_x, normalized_y, image_width, image_height):
    
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        
        return x_px, y_px