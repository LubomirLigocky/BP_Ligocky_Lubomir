import time
import math

from exercise_poses.helper_poses.poses_arms import ArmsPose

from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp

import cv2

from exercise_poses.helper_poses.poses_legs import LegsPose
from exercise_poses.helper_poses.poses_sit import SitPose

class ChairCirclingPose(ExerciseBase):

    right_shoulder_boundary = None
    left_shoulder_boundary = None

    is_sitting_phase = False
    is_standing_phase = False
  
    is_left_side_phase = False
    is_behind_chair_phase = False

    is_right_side_phase = False

    is_forward = False
    is_sitting_again = False

    distance_from = None
    distances_avg = []
    

    def reset_chair_phases(self):
        self.is_standing_phase = False
        
        self.is_left_side_phase = False
        self.is_behind_chair_phase = False

        self.is_right_side_phase = False
        self.is_forward = False
        self.is_sitting_again = False

    
    def __init__(self):
        super().__init__()
        self.arms_poses = ArmsPose()
        self.legs_poses = LegsPose()
        self.sit_poses = SitPose()

        self.curr_exercise_name = "chair_circling_exercise"
        self.is_high = False
        self.message_sent = ''
    
    def get_avg_distance(self, landmarks, depth_frame_np):
        left_shoulder = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Convert normalized coordinates to pixel positions
        left_pixel = (int(left_shoulder.x * 1280), int(left_shoulder.y * 720))
        right_pixel = (int(right_shoulder.x * 1280), int(right_shoulder.y * 720))

        # Access depth values directly from the NumPy array
        depth_left = depth_frame_np[left_pixel[1], left_pixel[0]] / 1000.0  # Convert mm to meters
        depth_right = depth_frame_np[right_pixel[1], right_pixel[0]] / 1000.0

        return (depth_left + depth_right) / 2

    def is_behind_chair(self, current_distance):
        return current_distance > self.distance_from

    def is_in_front_of_chair(self, current_distance):
        return current_distance <= self.distance_from

    def is_left_of_chair(self, nose_x):
        return nose_x > self.left_shoulder_boundary

    def is_right_of_chair(self, nose_x):
        return nose_x < self.right_shoulder_boundary

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth_frame):
        
        left_hip = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        
        self.angle_left = self.calculate_angle(left_ankle, left_knee, left_hip)
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)


        if self.is_sitting_phase is False:
              
            if  (25 < self.angle_left <= 172):
                distance = self.get_avg_distance(landmarks, depth_frame)
                if distance != 0 and self.distance_from == None:
                    self.distances_avg.append(distance)

                if self.check_correct_pose_timer(1.5):
                    self.is_sitting_phase = True
                
                    
                    if self.distance_from == None:
                        self.left_shoulder_boundary = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x
                        self.right_shoulder_boundary = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x

                        self.distance_from = sum(self.distances_avg) / float(len(self.distances_avg))
                    
                    exercise_label_signal.emit("Clovek_sa_ma_postavit")

                    self.message_sent = ''
                    self.wrong_pose_time_treshold = None
            else:
                self.correct_pose_time_treshold = None
                emit_msg = "Clovek_nesedi"
                
                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(2, False):

                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
    
             
                
        elif self.is_sitting_phase is True and self.is_standing_phase is False:
            if 168 < self.angle_left:
                if self.check_correct_pose_timer(0.75):
                    self.is_standing_phase = True
                    exercise_label_signal.emit("Clovek ma ist do lava")
                    self.wrong_pose_time_treshold = None
            else:
                self.correct_pose_time_treshold = None
                emit_msg = "Clovek_sa_ma_postavit"
                
                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(4.5, False):

                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
        
        elif self.is_standing_phase is True and self.is_left_side_phase is False:
            
            nose_landmark = landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value].x
            print(nose_landmark, self.left_shoulder_boundary )
            
            if self.is_left_of_chair(nose_landmark):
                if self.check_correct_pose_timer(0.05):
                    exercise_label_signal.emit("Clovek musi ist dozadu")
                    self.is_left_side_phase = True
                    self.wrong_pose_time_treshold = None
                    
            else:
                emit_msg = "Clovek_musi_ist_dolava"
                self.correct_pose_time_treshold = None
                
                if self.message_sent != emit_msg:
                    if self.check_wrong_pose_timer(4.5, False):
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None

        elif self.is_left_side_phase is True and self.is_behind_chair_phase is False:

            distance_behind = self.get_avg_distance(landmarks, depth_frame)
    
            print("distance_behind:", distance_behind, "distance_from:" ,self.distance_from)
          
            
            if self.is_behind_chair(distance_behind*2):
                if self.check_correct_pose_timer(0.05):
                    self.is_behind_chair_phase = True
                    self.wrong_pose_time_treshold = None
            else:
                emit_msg = "Clovek_musi_ist_dozadu"
                self.correct_pose_time_treshold = None
                exercise_label_signal.emit(emit_msg + str(distance_behind))
                if self.message_sent != emit_msg:
                    
                    if self.check_wrong_pose_timer(3.5, False):
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                     
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
        
        
        
        elif self.is_behind_chair_phase is True and self.is_right_side_phase is False:
            nose_landmark = landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value].x
            distance_behind = self.get_avg_distance(landmarks, depth_frame)

            if self.is_right_of_chair(nose_landmark) and nose_landmark < self.right_shoulder_boundary:
                if self.check_correct_pose_timer(0.25):
                    exercise_label_signal.emit("Clovek musi ist dopredu")
                    self.is_right_side_phase = True
                    self.wrong_pose_time_treshold = None
                    self.distance_from = self.get_avg_distance(landmarks, depth_frame)
            else:
              
                emit_msg = "Clovek_musi_ist_doprava"
                self.correct_pose_time_treshold = None

                if self.message_sent != emit_msg:
                    if self.check_wrong_pose_timer(5, False):
                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
        
        elif self.is_right_side_phase is True and self.is_sitting_again is False:
            
            if ( 25 < self.angle_left <= 172):
                if self.check_correct_pose_timer(0.75):
                    exercise_label_signal.emit("Sadol si ")
                    stage_signal.emit("up", "chair_circling", self.camera_exerice_score)
                    self.exercise_lock = True
                    self.wrong_pose_time_treshold = None
                    self.is_sitting_again = True     
            else:
                emit_msg = "Clovek_musi_ist_dopredu"
                if self.message_sent != emit_msg:

                    if self.check_wrong_pose_timer(3.5, False):

                        stage_signal.emit("warning", emit_msg, self.camera_exerice_score)
                        self.exercise_lock = True
                        exercise_label_signal.emit(emit_msg)
                        self.message_sent = emit_msg
                        self.wrong_pose_time_treshold = None
        
        if  self.is_sitting_again == True:
            score_signal.emit(True)
            self.camera_exerice_score += 1
            self.reset_chair_phases()
        

                      