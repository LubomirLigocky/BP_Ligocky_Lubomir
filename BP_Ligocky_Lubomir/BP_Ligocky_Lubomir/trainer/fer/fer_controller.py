import cv2
from datetime import datetime

class FerController:
    detectedEmotion = None

    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
         
        self.em_counter = 0
        self.em_lim = 20
        self.em_buffer = []        

        self.domimant_em_text = ""
        self.dominant_conf_text = ""
        
        self.limit = False
        self.prev_e = ""
        self.curr_e = ""
        

    def detectEmotion(self, color_image):

        frame, emotions= self.fer_model.recognizeEmotion(color_image)
         
        if len(emotions):
            # print("softmax out:", emotions)
            if self.em_counter == self.em_lim:
                self.em_buffer.pop(0)
                self.em_counter = self.em_counter - 1
                
            self.domimant_em_text, self.dominant_conf_text = self.fer_model.getDominantConfidence(emotions)
            frame = self.fer_model.createRectangleText(frame, (self.domimant_em_text + self.dominant_conf_text))

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
            self.em_buffer.append({'emotions': emotions, 'timestamp': timestamp})
            self.em_counter = self.em_counter + 1
          

        else:
           if self.em_counter > 0:
                self.em_counter = self.em_counter - 1 
        
        # print("Counter",self.em_counter)
        return frame

    
    def aggregateEmotions(self, penalty_factor=0.08):
        if not self.em_buffer or self.em_counter == 0:
            print("Prazdny buffer")
            return "Neutral"

        T = len(self.em_buffer)
        emotion_classes = self.fer_model.DICT_EMO.keys()
        cumulative_scores = {self.fer_model.DICT_EMO[e]: 0.0 for e in emotion_classes}

        # Get latest timestamp
        latest_time = datetime.strptime(self.em_buffer[-1]['timestamp'], "%Y-%m-%d %H:%M:%S")

        for entry in self.em_buffer:
            entry_time = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
            time_diff = (latest_time - entry_time).total_seconds()  # difference in seconds
            time_penalty = penalty_factor * time_diff

            for e_idx in emotion_classes:
                emotion_name = self.fer_model.DICT_EMO[e_idx]
                weight = entry['emotions'][0][e_idx]  # direct access to ndarray
                penalized = weight - time_penalty
                if penalized < 0:
                    penalized = 0
                cumulative_scores[emotion_name] += penalized

        print("Cumulative scores:", cumulative_scores)
        final_emotion = max(cumulative_scores, key=cumulative_scores.get)

        return final_emotion
