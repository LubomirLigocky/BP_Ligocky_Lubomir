import time
import math

from exercise_poses.helper_poses.poses_arms import ArmsPose

from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp
import cv2


class PredpazovanieExercisePose(ExerciseBase):

    predpazovanie_sent00 = False
    predpazovanie_sent01 = False
    predpazovanie_sent02 = False

    width_threshold= 0.082 
    height_threshold=0.135
    vertical_offset= 0.085

    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.curr_exercise_name = "predpazovanie_exercise"
    
    def reset_predpazovanie_signal(self):
        self.predpazovanie_sent00 = False
        self.predpazovanie_sent01 = False
        self.predpazovanie_sent02 = False
    

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth):
        # print(self.arms_poses.is_arms_raised_forward(landmarks))
        is_arms_raised_forward, arms = self.arms_poses.is_arms_raised_forward(landmarks, self.width_threshold)

        if self.predpazovanie_sent00 == False:
                
                stage_signal.emit("00,", "predpazovanie_fullfilled", self.camera_exerice_score)
                self.exercise_lock = True 
                exercise_label_signal.emit("Clovek ma predpazit.")
                self.predpazovanie_sent00 = True

        
        if self.predpazovanie_sent01 == False and self.predpazovanie_sent00 == True:
            
            if is_arms_raised_forward is True:
                self.base_pose_time_treshold = None

                if self.correct_pose_time_treshold == None:
                        self.correct_pose_time_treshold = time.time()
                
                elif time.time() - self.correct_pose_time_treshold >= 0.5:

                    stage_signal.emit("01,", "predpazovanie_fullfilled", self.camera_exerice_score)
                    self.exercise_lock = True
                    exercise_label_signal.emit("Clovek ma pripazit.")

                    self.predpazovanie_sent01 = True

                    self.wrong_pose_time_treshold = None
                    self.correct_pose_time_treshold = None
                    self.message_sent = ''
                
            
            elif self.arms_poses.is_arms_put_down(landmarks, 0.1):
                self.wrong_pose_time_treshold = None
                self.correct_pose_time_treshold = None
                
                if self.check_base_pose_timer(1.5):
                    self.message_sent  = 'Base_pos'
                    stage_signal.emit("warning",  self.message_sent , self.camera_exerice_score)
                    self.exercise_lock = True
                    exercise_label_signal.emit( self.message_sent )

                    self.base_pose_time_treshold = 0           

            else :
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None


                emit_msg = self.arms_poses.wrong_arms_pose_warning(self.curr_exercise_name, arms, self, self.width_threshold)

                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(2.5, False):
                       
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None

        
        if self.predpazovanie_sent02 == False and self.predpazovanie_sent01 == True and self.predpazovanie_sent00 == True:
            
            if self.arms_poses.is_arms_put_down(landmarks, 0.1):
                stage_signal.emit("02,", "predpazovanie_fullfilled", self.camera_exerice_score)
                self.exercise_lock = True
                self.predpazovanie_sent02= True
                self.base_pose_time_treshold = None
                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_predpazovanie_signal()
                
            elif self.check_base_pose_timer(1.5):
                self.message_sent  = 'Base_pos_back'
                stage_signal.emit("warning",  self.message_sent , self.camera_exerice_score)
                self.exercise_lock = True
                exercise_label_signal.emit( self.message_sent )

                self.base_pose_time_treshold = 0      
        
        return 
    
    def show_regions(self, image, landmarks, width_threshold, height_threshold, vertical_offset):
        
        if image is None:
            return

        image_height, image_width = image.shape[:2]
        shoulder_indices = [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, 
                        mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]

        for shoulder_index in shoulder_indices:
            shoulder = landmarks.landmark[shoulder_index]
            
            # Calculate bounds
            left_bound = shoulder.x - width_threshold
            right_bound = shoulder.x + width_threshold
            top_bound = shoulder.y - height_threshold 
            bottom_bound = shoulder.y + vertical_offset 

            # Convert to pixel coordinates
            rect_left = int(left_bound * image_width)
            rect_right = int(right_bound * image_width)
            rect_top = int(top_bound * image_height)
            rect_bottom = int(bottom_bound * image_height)

            # Draw rectangle
            color = (0, 255, 255)  # Green
            thickness = 2
            cv2.rectangle(image, 
                        (rect_left, rect_top),
                        (rect_right, rect_bottom),
                        color,
                        thickness)
            
    
    def visual_debug_up(self, image, landmarks):
        self.show_regions(image, landmarks, self.width_threshold, self.height_threshold, self.vertical_offset)
    

    def warning_message(self, both_arms, side_arm, right_arm_up, left_arm_up, right_arm_low,left_arm_low, right_arm_aside, left_arm_aside):
        if both_arms:
            if right_arm_up and left_arm_up:
                if right_arm_aside and left_arm_aside:
                    return "Predpazene_ruky_vysoko_a_odseba"
                elif right_arm_aside or left_arm_aside:
                    return "Predpazene_ruky_vysoko_a_nespravne"
                else:
                    return "Predpazene_ruky_vysoko"
            
            if right_arm_low and left_arm_low:
                if right_arm_aside and left_arm_aside:
                    return "Predpazene_ruky_nizko_a_odseba"
                elif right_arm_aside or left_arm_aside:
                    "Predpazene_ruky_nizko_a_nespravne"
                else:
                    return "Predpazene_ruky_nizko"
            else:
                if (right_arm_up and left_arm_low) or (left_arm_up and right_arm_low):
                    return  "Predpazene_ruky_zle"
                elif right_arm_aside or left_arm_aside:
                    return  "Predpazene_ruky_priliz_od_seba"
        else:
            if side_arm == "right":
                if right_arm_up:
                    if right_arm_aside:
                        return "Prava_ruka_vysoko_a_od_tela"
                    else:
                        return "Prava_ruka_vysoko"
                if right_arm_low:
                    if right_arm_aside:
                        return "Prava_ruka_nizko_a_od_tela"
                    else:
                        return "Prava_ruka_nizko"
                else:
                    if right_arm_aside:
                        return "Prava_ruka_od_tela"
            
            if side_arm == "left":
                if left_arm_up:
                    if left_arm_aside:
                        return "Lava_ruka_vysoko_a_od_tela"
                    else:
                        return "Lava_ruka_vysoko"
                if left_arm_low:
                    if left_arm_aside:
                        return "Lava_ruka_nizko_a_od_tela"
                    else:
                        return "Lava_ruka_nizko"
                else:
                    if left_arm_aside:
                        return "Lava_ruka_od_tela"
        return "Chyba" 