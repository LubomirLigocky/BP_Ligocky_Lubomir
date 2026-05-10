import time
import math

from exercise_poses.helper_poses.poses_arms import ArmsPose

from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp

import cv2

from exercise_poses.helper_poses.poses_sit import SitPose

class ArmSitCirclingPose(ExerciseBase):

    width_threshold= 0.082 
    height_threshold=0.135
    vertical_offset= 0.085
    were_arms_forward = False
    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.sit_poses = SitPose()
        self.curr_exercise_name = "arm_sit_circling_exercise"
        self.is_high = False

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth = None, frame = None):

        is_arms_raised_down = self.sit_poses.is_in_base_forefooting_position(landmarks)
        
        if self.stage_up is False:
            self.stage_up = True
            exercise_label_signal.emit("Otoč ruky hore")
            stage_signal.emit("up", "arm_sit_circling", self.camera_exerice_score)
            self.exercise_lock = True

        elif self.stage_up  and self.stage_down is False:

            is_arms_raised_up = self.arms_poses.arms_raised_up(landmarks)

            if is_arms_raised_up:
                
                self.base_pose_time_treshold = None
                self.wrong_pose_time_treshold = None

                if self.check_correct_pose_timer(0.25):
                    self.stage_down = True
                    exercise_label_signal.emit("Otoč dole ruky")
                    stage_signal.emit("down", "arm_sit_circling", self.camera_exerice_score)
                    self.exercise_lock = True
                   
                    self.correct_pose_time_treshold = None
                    self.message_sent = ''
            
            else:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None

                emit_msg = "ZLE_hore"

                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(1.5, False):

                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None

        elif self.stage_up and self.stage_down:
            
            if is_arms_raised_down:
                if self.check_correct_pose_timer(0.35):
                    score_signal.emit(True)
                    self.camera_exerice_score += 1
                    self.stage_up = False
                    self.stage_down = False
            else:
                self.base_pose_time_treshold = None
                self.correct_pose_time_treshold = None
                emit_msg = "ZLE_dole"
                if self.message_sent != emit_msg:
                    if self.check_wrong_pose_timer(1.5, False):
                        self.message_sent = emit_msg
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.wrong_pose_time_treshold = None
