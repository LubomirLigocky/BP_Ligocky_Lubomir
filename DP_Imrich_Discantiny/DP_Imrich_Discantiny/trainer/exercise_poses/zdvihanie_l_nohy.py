import cv2

from exercise_poses.helper_poses.poses_arms import ArmsPose
from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp


class LeftLegLiftPose(ExerciseBase):

    y_threshold=0.05
    wrist_shoulder_distance_threshold = 0.1
    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.curr_exercise_name = "tpose_exercise"
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):

        left_shoulder = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]

        # Calculate angle
        self.angle = self.calculate_angle(left_shoulder, left_hip, left_knee)

        # check if the angle is within the threshold and write the result in label
        if self.angle > 170:
            self.pose_finished = True
            if self.stage_up == False:
                self.stage_down = True
                exercise_label_signal.emit("NOHA HORE")
                if self.stage_down_message_sent == False:
                    if self.lift_left_leg_exercise_finished == False:
                        stage_signal.emit(
                            "down", "left_leg", self.camera_exerice_score)
                        
                    self.stage_down_message_sent = True
        elif 120 < self.angle < 170:
            if self.stage_up == False and self.stage_down == True:
                exercise_label_signal.emit("NOHA HORE")
            elif self.stage_up == True and self.stage_down == True:
                exercise_label_signal.emit("NOHA DOLE")
        elif self.angle < 120:
            self.pose_finished = False
            if self.stage_down == True:
                self.stage_up = True
                exercise_label_signal.emit("NOHA DOLE")
                if self.stage_up_message_sent == False:
                    if self.lift_left_leg_exercise_finished == False:
                        stage_signal.emit(
                            "up", "left_leg", self.camera_exerice_score)
                        
                    self.stage_up_message_sent = True
        else:
            self.pose_finished = False
            exercise_label_signal.emit("ZLÁ POZÍCIA")

        if self.stage_down == True and self.stage_up == True and self.pose_finished == True:
            score_signal.emit(True)
            self.camera_exerice_score += 1
            self.stage_up = False
            self.stage_down = False
            self.stage_up_message_sent = False
            self.stage_down_message_sent = False
    
  

