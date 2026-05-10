import time
import math

from exercise_poses.helper_poses.poses_arms import ArmsPose

from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp

import cv2

class SquatExercisePose(ExerciseBase):

    width_threshold= 0.082 
    height_threshold=0.135
    vertical_offset= 0.085
    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.curr_exercise_name = "squat_exercise"
        self.is_high = False
        self.done_pose_correction = True

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth = None, frame = None):
       
        self.last_pose_finished = self.pose_finished
        if not landmarks:
            print("No Landmarks")
            return
        # Get coordinates of shoulders, elbows and wrists
        left_hip = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]
        right_ankle = [landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y]
        
        # Check if ankles arent too close to each other
        if self.camera_exerice_score < 4:
            if abs(left_ankle[0] - right_ankle[0]) <= 0.05 and self.pose_correction is False:

                exercise_label_signal.emit("Nema ROZOSTUP")
                stage_signal.emit("warning", "squat_rozpaz", self.camera_exerice_score)
                self.pose_correction = True
                self.exercise_lock = True

            elif self.pose_correction is True and abs(left_ankle[0] - right_ankle[0]) >= 0.085:
                exercise_label_signal.emit("ROZOSTUP SA")
                self.pose_correction = False
                self.done_pose_correction = True
                stage_signal.emit("warning_corr", "squat_rozpaz_oprava", self.camera_exerice_score)
                self.exercise_lock = True
            elif abs(left_ankle[0] - right_ankle[0]) < 0.085 and self.pose_correction:
                exercise_label_signal.emit("Nema ROZOSTUP")
                stage_signal.emit("warning", "squat_rozpaz", self.camera_exerice_score)
        else:
            self.pose_correction = False
        if self.pose_correction is False:
            
            self.angle_left = self.calculate_angle(left_ankle, left_knee, left_hip)  # Get the angle

            # check if the angle is within the threshold and write the result in label

            if 175 < self.angle_left: # 165 je taka bulharska konstanta na poddrep - ked je to <178; 182>, tak clovek stoji
                self.pose_finished = True
                
                if self.stage_down is False and self.stage_up is False:
                    self.stage_up = True
                    exercise_label_signal.emit("DOLE")
                    stage_signal.emit("up", "squat", self.camera_exerice_score)
                    self.exercise_lock = True
                
                elif self.stage_up and self.arms_poses.is_arms_put_down(landmarks, 0.1):
                    self.wrong_pose_time_treshold = None
                    self.correct_pose_time_treshold = None
                    print("before emit")
                    if self.done_pose_correction or self.check_base_pose_timer(3.0):
                        self.done_pose_correction = False
                        self.message_sent = 'Base_pos'
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(self.message_sent + " DOLE")
                        
                        self.base_pose_time_treshold = 0
                    else:
                        print("fail")

            elif 173 < self.angle_left <= 175 and self.stage_up:
                self.base_pose_time_treshold = None
                emit_msg =  "squat_zly_drep"
                self.is_high = True

                if self.message_sent != emit_msg:
                    if self.check_wrong_pose_timer(0.5, False):

                        
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        
                        self.wrong_pose_time_treshold = None
                        self.is_high = False
                

            elif 25 < self.angle_left <= 173:
                if self.stage_down is True and self.stage_up is True and self.check_base_pose_timer(2.5):
                   
                    self.message_sent = 'Base_pos_back'
                    stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                    self.exercise_lock = True
                    exercise_label_signal.emit(self.message_sent)
                    self.base_pose_time_treshold = 0
                    self.base_pose_time_treshold= None
                
                elif self.stage_down is False:
                    
                    if self.is_high is True:
                        self.is_high = False
                        self.wrong_pose_time_treshold = None

                    self.base_pose_time_treshold = None
                    
                    exercise_label_signal.emit("JE V DREPE")
                    arms_raised_forward, arms = self.arms_poses.is_arms_raised_forward(landmarks, self.width_threshold)

                    if arms_raised_forward:
                        exercise_label_signal.emit("PREDPAŽIL")
                        self.pose_finished = False
                        
                        if self.stage_up is True and self.stage_down is False:
                            self.stage_down = True
                            exercise_label_signal.emit("HORE")
                            stage_signal.emit("down", "squat", self.camera_exerice_score)
                            self.exercise_lock = True
                            
                            self.wrong_pose_time_treshold = None
                            self.message_sent = ''       
                    
                    else:
                        emit_msg = self.arms_poses.wrong_arms_pose_warning(self.curr_exercise_name, arms, self, self.width_threshold)
                        print(emit_msg)
                        if self.message_sent != emit_msg:
                            
                            if self.check_wrong_pose_timer(0.5, False):
                                stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                                self.exercise_lock = True
                                exercise_label_signal.emit(emit_msg)
                                self.message_sent = emit_msg
                                self.wrong_pose_time_treshold = None
            else:
                self.pose_finished = False
                exercise_label_signal.emit("ZLÁ POZÍCIA")

        if self.stage_down == True and self.stage_up == True and self.pose_finished == True:
            score_signal.emit(True)
            self.camera_exerice_score += 1
            self.stage_up = False
            self.stage_down = False
    
    
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
    
    
    def warning_message(self, both_arms, side_arm, right_arm_up, left_arm_up, right_arm_low,left_arm_low, right_arm_aside, left_arm_aside, front_or_back: str="front"):
        if both_arms:
            if right_arm_up and left_arm_up:
                if right_arm_aside or left_arm_aside:
                    return "V_drepe_predpazene_ruky_vysoko_a_odseba"
                else:
                    return "V_drepe_predpazene_ruky_vysoko"
            elif right_arm_low and left_arm_low:
                if right_arm_aside or left_arm_aside:
                    return "V_drepe_predpazene_ruky_nizko_a_odseba"
                else:
                    return "V_drepe_predpazene_ruky_nizko"
            else:
                if (right_arm_up and left_arm_low) or (left_arm_up and right_arm_low):
                    return  "V_drepe_predpazene_ruky_zle"
                elif right_arm_aside or left_arm_aside:
                    return  "V_drepe_predpazene_ruky_priliz_od_seba"   
        elif side_arm == "right":
            if right_arm_up:
                return "V_drepe_prava_ruka_vysoko"
            elif right_arm_low:
                return "V_drepe_prava_ruka_nizko"
            else:
                return "V_drepe_prava_ruka_nespravne"
        elif side_arm == "left":
            if left_arm_up:
                return "V_drepe_lava_ruka_vysoko"
            elif left_arm_low:
                return "V_drepe_lava_ruka_nizko"
            else:
                return "V_drepe_lava_ruka_nespravne"
        return "Chyba" 