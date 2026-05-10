import time
import math
from exercise_poses.forefooting_exercise import BasicForefootingExercise
import cv2

import mediapipe as mp

class ForefootingPredpazovaniePose(BasicForefootingExercise):
    height_threshold=0.16
    vertical_offset= 0.085
    width_threshold= 0.091
   
    def __init__(self):
        super().__init__()
        self.curr_exercise_name = "forefooting_predpazovanie_exercise"
        
        self.leg_wrong = False
        self.arm_wrong = False
        
        self.emit_msg_legs = ''
        self.emit_msg_arms = ''

    
    def reset_warnings(self):
        self.leg_wrong = False
        self.arm_wrong = False
        
        self.emit_msg_legs = ''
        self.emit_msg_arms = ''

        self.message_sent = ''
        self.correct_pose_time_treshold = None
        self.wrong_pose_time_treshold = None
        self.base_pose_time_treshold = None
    

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth):
      
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_right_leg_raised = self.legs_poses.is_right_leg_raised(landmarks)
        is_left_leg_raised = self.legs_poses.is_left_leg_raised(landmarks)
        arms_raised_forward, arms = self.arms_poses.is_arms_raised_forward(landmarks, self.width_threshold)


        if self.sit_forefooting_on_chair_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_predpazovanie_fullfilled",self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.exercise_lock = True
                
                self.wrong_pose_time_treshold = None
                self.sit_forefooting_on_chair_sent00 = True
            else:
                if self.check_wrong_pose_timer(2, False):
                    stage_signal.emit("warning", "Not_sitting",self.camera_exerice_score)
                    self.wrong_pose_time_treshold = 0
                    self.exercise_lock = True
        
        if self.sit_forefooting_on_chair_sent01 == False and self.sit_forefooting_on_chair_sent00 == True:
            
            if is_right_leg_raised is True and arms_raised_forward is True:
                    
                if self.correct_pose_time_treshold == None:
                    self.correct_pose_time_treshold = time.time()
                
                elif time.time() - self.correct_pose_time_treshold >= 0.45 :
                    stage_signal.emit("01,", "forefooting_predpazovanie_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                    exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                    
                    self.sit_forefooting_on_chair_sent01 = True
                    self.exercise_lock = True
                    self.reset_warnings()
            
            elif not is_right_leg_raised is True and self.sit_poses.is_in_base_forefooting_position(landmarks):
                
                self.correct_pose_time_treshold = None
                self.wrong_pose_time_treshold = None
                self.message_sent = ''
                
                if self.check_base_pose_timer(2.0):
                    exercise_label_signal.emit("In Base")
                    stage_signal.emit("warning", "In_Base_pos_right", self.camera_exerice_score)
                    self.base_pose_time_treshold = 0
                    self.exercise_lock = True

            elif is_right_leg_raised is False or arms_raised_forward is False:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                if is_right_leg_raised is False:
                    self.leg_wrong = True
                    self.emit_msg_legs = "ForefootingPred_a_zdvihni_pravu_nohu"

                elif self.leg_wrong is True:
                    self.leg_wrong = False
                    self.emit_msg_legs = ''

                if arms_raised_forward is False:
                    self.arm_wrong = True   
                    print(arms_raised_forward, arms)
                    self.emit_msg_arms = self.arms_poses.wrong_arms_pose_warning(self.curr_exercise_name, arms, self, self.width_threshold)
                        
                elif self.arm_wrong is True:
                    self.arm_wrong = False
                    self.emit_msg_arms = ''
                
                
                if self.emit_msg_legs + self.emit_msg_arms != self.message_sent:
                    
                    if self.check_wrong_pose_timer(2, False):

                        if self.emit_msg_legs + self.emit_msg_arms != self.message_sent:
                            self.message_sent = self.emit_msg_legs + self.emit_msg_arms
                            stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                            exercise_label_signal.emit(self.message_sent)
                            self.exercise_lock = True
                            self.wrong_pose_time_treshold = None
                        else:
                            return True

        if self.sit_forefooting_on_chair_sent02 == False and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
            if is_right_leg_raised is False and arms_raised_forward is False:
                stage_signal.emit("02,", "forefooting_predpazovanie_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_on_chair_sent02 = True
                self.exercise_lock = True

        if self.sit_forefooting_on_chair_sent03 == False and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
            
            if is_left_leg_raised is True and arms_raised_forward is True :
                    
                if self.correct_pose_time_treshold == None:
                    self.correct_pose_time_treshold = time.time()
                
                elif time.time() - self.correct_pose_time_treshold >= 0.45:
                    stage_signal.emit("03,", "forefooting_predpazovanie_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                    exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                    
                    self.sit_forefooting_on_chair_sent03 = True
                    self.exercise_lock = True
                    self.reset_warnings()

            elif not is_left_leg_raised and self.sit_poses.is_in_base_forefooting_position(landmarks):
                
                self.correct_pose_time_treshold = None
                self.wrong_pose_time_treshold = None
                self.message_sent = ''
                
                if self.check_base_pose_timer(2.0):
                    exercise_label_signal.emit("In Base")
                    self.exercise_lock = True
                    stage_signal.emit("warning", "In_Base_pos_left", self.camera_exerice_score)
                    self.base_pose_time_treshold = 0

            elif is_left_leg_raised is False or arms_raised_forward is False:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                if is_left_leg_raised is False:
                    self.leg_wrong = True
                    self.emit_msg_legs = "ForefootingPred_a_zdvihni_lavu_nohu"

                elif self.leg_wrong is True:
                    self.leg_wrong = False
                    self.emit_msg_legs = ''

                if arms_raised_forward is False:
                    self.arm_wrong = True   
                    print(arms_raised_forward, arms)
                    self.emit_msg_arms = self.arms_poses.wrong_arms_pose_warning(self.curr_exercise_name, arms, self, self.width_threshold)
                        
                elif self.arm_wrong is True:
                    self.arm_wrong = False
                    self.emit_msg_arms = ''
                
                if self.emit_msg_legs + self.emit_msg_arms != self.message_sent:
                
                    if self.check_wrong_pose_timer(2, False):
                        self.message_sent = self.emit_msg_legs + self.emit_msg_arms
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        exercise_label_signal.emit(self.message_sent)
                        self.exercise_lock = True

                        self.wrong_pose_time_treshold = None
                    else:
                        return True

        if self.sit_forefooting_on_chair_sent04 == False and self.sit_forefooting_on_chair_sent03 == True and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True :
            
            if is_left_leg_raised is False and arms_raised_forward is False:
                stage_signal.emit("04,", "forefooting_predpazovanie_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_on_chair_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.exercise_lock = True
                self.reset_forefooting_on_chair_signal()
        
        return True
    
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