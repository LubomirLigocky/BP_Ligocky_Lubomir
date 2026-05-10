import time
import cv2
import mediapipe as mp

from exercise_poses.forefooting_exercise import BasicForefootingExercise


class ForefootingRozpazovaniePose(BasicForefootingExercise):
    y_threshold=0.1
    wrist_shoulder_distance_threshold = 0.1


    def __init__(self):
        super().__init__()
        self.curr_exercise_name = "forefooting_rozpazovanie_exercise"

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
        arms_in_line_for_lateral_raises, arms_coordinates, is_wrist_close = self.arms_poses.is_arms_in_tpose(landmarks,  self.y_threshold, self.wrist_shoulder_distance_threshold)

        if self.sit_forefooting_on_chair_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_rozpazovanie_fullfilled", self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu a rozpazit.")
                self.exercise_lock = True
                self.wrong_pose_time_treshold = None
                self.sit_forefooting_on_chair_sent00 = True
            else:
                if self.check_wrong_pose_timer(2.5, False):
                    stage_signal.emit("warning", "Not_sitting", self.camera_exerice_score)
                    self.exercise_lock = True
                    self.wrong_pose_time_treshold = 0
        
        if self.sit_forefooting_on_chair_sent01 == False and self.sit_forefooting_on_chair_sent00 == True:

            if is_right_leg_raised is True and arms_in_line_for_lateral_raises is True:
                
                if self.correct_pose_time_treshold == None:
                    self.correct_pose_time_treshold = time.time()
                
                elif time.time() - self.correct_pose_time_treshold >= 0.35:   
                    stage_signal.emit("01,", "forefooting_rozpazovanie_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                    self.exercise_lock = True
                    exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                    
                    self.sit_forefooting_on_chair_sent01 = True
                    
                    self.reset_warnings()
            
            elif not is_right_leg_raised and self.sit_poses.is_in_base_forefooting_position(landmarks):
                
                self.correct_pose_time_treshold = None
                self.wrong_pose_time_treshold = None
                self.message_sent = ''
                
                if self.check_base_pose_timer(2.0):
                    exercise_label_signal.emit("In Base")
                    stage_signal.emit("warning", "In_Base_pos_right", self.camera_exerice_score)
                    self.exercise_lock = True
                    self.base_pose_time_treshold = 0

            elif is_right_leg_raised is False or arms_in_line_for_lateral_raises is False:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                if is_right_leg_raised is False:
                    self.leg_wrong = True
                    self.emit_msg_legs = "ForefootingRoz_a_zdvihni_pravu_nohu"

                elif self.leg_wrong is True:
                    self.leg_wrong = False
                    self.emit_msg_legs = ''

                if arms_in_line_for_lateral_raises is False:
                    self.arm_wrong = True   
                    self.emit_msg_arms = self.arms_poses.wrong_tpose_pose_warning(arms_coordinates)
                        
                elif self.arm_wrong is True:
                    self.arm_wrong = False
                    self.emit_msg_arms = ''
                
                if self.wrong_pose_time_treshold == None:
                    self.wrong_pose_time_treshold = time.time()
                
                elif time.time() - self.wrong_pose_time_treshold >= 2.0 and self.wrong_pose_time_treshold > 0:
                    print('emit_msg_arms', self.emit_msg_arms )
                    print('emit_msg_legs', self.emit_msg_legs)

                    if self.emit_msg_legs + self.emit_msg_arms != self.message_sent:
                        self.message_sent = self.emit_msg_legs + self.emit_msg_arms
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(self.message_sent)
                        
                        self.wrong_pose_time_treshold = None
                    else:
                        return True

        if self.sit_forefooting_on_chair_sent02 == False and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True: 
            if is_right_leg_raised is False and arms_in_line_for_lateral_raises is False:
                stage_signal.emit("02,", "forefooting_rozpazovanie_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                self.exercise_lock = True
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_on_chair_sent02 = True

        if self.sit_forefooting_on_chair_sent03 == False and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
            
            if is_left_leg_raised is True and arms_in_line_for_lateral_raises is True:
                
                if self.correct_pose_time_treshold == None:
                    self.correct_pose_time_treshold = time.time()

                elif time.time() - self.correct_pose_time_treshold >= 0.35:
                    stage_signal.emit("03,", "forefooting_rozpazovanie_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                    self.exercise_lock = True
                    exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                    self.sit_forefooting_on_chair_sent03 = True
                    
                    self.reset_warnings()
            
            elif not is_left_leg_raised and  self.sit_poses.is_in_base_forefooting_position(landmarks):
                
                self.correct_pose_time_treshold = None
                self.wrong_pose_time_treshold = None
                self.message_sent = ''
                
                if self.check_base_pose_timer(2.0):
                    exercise_label_signal.emit("In Base")
                    stage_signal.emit("warning", "In_Base_pos_left", self.camera_exerice_score)
                    self.exercise_lock = True
                    self.base_pose_time_treshold = 0
            
            elif is_left_leg_raised is False or arms_in_line_for_lateral_raises is False:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                if is_left_leg_raised is False:
                    self.leg_wrong = True
                    self.emit_msg_legs = "ForefootingRoz_a_zdvihni_lavu_nohu_"

                elif self.leg_wrong is True:
                    self.leg_wrong = False
                    self.emit_msg_legs = ''

                if arms_in_line_for_lateral_raises is False:
                    self.arm_wrong = True   
                    self.emit_msg_arms = self.arms_poses.wrong_tpose_pose_warning(arms_coordinates)
                        
                elif self.arm_wrong is True:
                    self.arm_wrong = False
                    self.emit_msg_arms = ''
                
                if self.wrong_pose_time_treshold == None:
                    self.wrong_pose_time_treshold = time.time()
                
                elif time.time() - self.wrong_pose_time_treshold >= 2.0 and self.wrong_pose_time_treshold > 0:
                    print('emit_msg_arms', self.emit_msg_arms, self.arm_wrong)
                    print('emit_msg_legs', self.emit_msg_legs, self.leg_wrong)

                    if self.emit_msg_legs + self.emit_msg_arms != self.message_sent:
                        self.message_sent = self.emit_msg_legs + self.emit_msg_arms
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(self.message_sent)
                        
                        self.wrong_pose_time_treshold = None
                    else:
                        return True
                 

        if self.sit_forefooting_on_chair_sent04 == False and self.sit_forefooting_on_chair_sent03 == True and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
            if is_left_leg_raised is False and arms_in_line_for_lateral_raises is False:
                stage_signal.emit("04,", "forefooting_rozpazovanie_fullfilled", self.camera_exerice_score)
                self.exercise_lock = True
                self.sit_forefooting_on_chair_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_on_chair_signal()
        
        return True
    

    def visual_debug_up(self, image, landmarks):
        self.show_regions(image, landmarks)

    def show_regions(self, frame, landmarks):
        if frame is None:
            return

        image_height, image_width = frame.shape[:2]

        threshold_y = int(self.y_threshold * image_height)

        shoulder_indices = [
            mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value,
            mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
        ]

        if not landmarks:
            return  # Handle case where pose landmarks are not detected

        left_shoulder = landmarks.landmark[shoulder_indices[0]]
        right_shoulder = landmarks.landmark[shoulder_indices[1]]

        # Convert normalized coordinates to pixel values
        left_shoulder_x = int(left_shoulder.x * image_width)
        left_shoulder_y = int(left_shoulder.y * image_height)
        right_shoulder_x = int(right_shoulder.x * image_width)
        right_shoulder_y = int(right_shoulder.y * image_height)

        cv2.rectangle(
            frame,
            (0, right_shoulder_y - threshold_y),  # Top-left corner
            (right_shoulder_x, right_shoulder_y + threshold_y),  # Bottom-right corner
            (0, 0, 255),  # Color (red in BGR)
            2  # Thickness of the border
        )

        # Draw right rectangle (from right shoulder to right edge)
        cv2.rectangle(
            frame,
            (left_shoulder_x, left_shoulder_y - threshold_y),  # Top-left corner
            (image_width, left_shoulder_y + threshold_y),  # Bottom-right corner
            (0, 0, 255),  # Color (red in BGR)
            2  # Thickness of the border
        )