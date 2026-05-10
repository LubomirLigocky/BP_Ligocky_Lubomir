import cv2

from exercise_poses.helper_poses.poses_arms import ArmsPose
from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp


class TposeExercisePose(ExerciseBase):

    y_threshold=0.05
    wrist_shoulder_distance_threshold = 0.1
    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.curr_exercise_name = "tpose_exercise"
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth):

        self.last_pose_finished = self.pose_finished
        is_in_tpose, arms_coordinates, is_wrist_close = self.arms_poses.is_arms_in_tpose(landmarks, self.y_threshold, self.wrist_shoulder_distance_threshold)
       
        
        if self.stage_up is False and self.stage_down is False:
              
            # Check if the angle is within the threshold and write the result in label
            if self.arms_poses.is_arms_put_down(landmarks, 0.1) or self.camera_exerice_score == 0:
               
                exercise_label_signal.emit("Upaž ruky")         
                stage_signal.emit("down", "tpose", self.camera_exerice_score)
                self.exercise_lock = True
                self.base_pose_time_treshold = None
                    
                self.stage_down = True
            
            elif self.check_base_pose_timer(2.5):
                self.message_sent = 'Base_pos_back'
                stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                self.exercise_lock = True
                exercise_label_signal.emit(self.message_sent)

                self.base_pose_time_treshold = 0

        elif self.stage_down == True :
            
            if is_in_tpose:
                
                self.base_pose_time_treshold = None
                self.wrong_pose_time_treshold = None

                if self.check_correct_pose_timer(0.5):
                    
                    self.stage_up = True
                    exercise_label_signal.emit("Pripaž ruky")
                    stage_signal.emit("up", "tpose", self.camera_exerice_score)
                    self.exercise_lock = True

                    # self.stage_up_message_sent = True
                    self.correct_pose_time_treshold = None
                    
                    self.message_sent = ''

            elif self.arms_poses.is_arms_put_down(landmarks, 0.1):
                self.wrong_pose_time_treshold = None
                self.correct_pose_time_treshold = None
                
                if self.check_base_pose_timer(2.5):
                    self.message_sent = 'Base_pos'
                    stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                    self.exercise_lock = True
                    exercise_label_signal.emit(self.message_sent)

                    self.base_pose_time_treshold = 0

            else:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                emit_msg = self.arms_poses.wrong_tpose_pose_warning(arms_coordinates)

                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(1.5, False):

                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
        
                
        if self.stage_down == True and self.stage_up == True:
            score_signal.emit(True)
            self.camera_exerice_score += 1
            self.stage_up = False
            self.stage_down = False
    
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

        wrist_indices = [
            mp.solutions.pose.PoseLandmark.LEFT_WRIST.value,
            mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value
        ]

        elbow_indices = [
            mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value,
            mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value
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
            (0+ 125, right_shoulder_y - threshold_y),  # Top-left corner
            (right_shoulder_x, right_shoulder_y + threshold_y),  # Bottom-right corner
            (0, 0, 255),  # Color (red in BGR)
            2  # Thickness of the border
        )

        # Draw right rectangle (from right shoulder to right edge)
        cv2.rectangle(
            frame,
            (left_shoulder_x, left_shoulder_y - threshold_y),  # Top-left corner
            ( image_width -125 , left_shoulder_y + threshold_y),  # Bottom-right corner
            (0, 0, 255),  # Color (red in BGR)
            2  # Thickness of the border
        )


        # # Draw circles around wrists, shoulders, and elbows
        # body_parts = wrist_indices + shoulder_indices + elbow_indices
        # for index in body_parts:
        #     part = landmarks.landmark[index]
        #     part_x = int(part.x * image_width)
        #     part_y = int(part.y * image_height)

        #     cv2.circle(
        #         frame,
        #         (part_x, part_y),  # Center of the circle
        #         int(self.wrist_shoulder_distance_threshold),  # Radius of the circle
        #         (255, 0, 0),  # Color (blue in BGR)
        #         2  # Thickness of the circle's border
        #     )
    


