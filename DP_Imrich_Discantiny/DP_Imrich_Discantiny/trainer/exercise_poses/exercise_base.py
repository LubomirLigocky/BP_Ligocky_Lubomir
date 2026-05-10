import numpy as np
import time

class ExerciseBase():
    exercise_lock = True

    curr_exercise_name = None
    curr_exercise_impl = None

    pose_warning = True
    pose_correction = False

    wrong_pose_time_treshold = None
    correct_pose_time_treshold = None
    base_pose_time_treshold = None

    camera_exerice_score = 0
    pose_finished = False
    last_pose_finished = False
    
    stage_up = False
    stage_down = False
  
    stage_up_message_sent = False
    stage_down_message_sent = False
  
    tpose_exercise_finished = False
   
    lift_left_leg_exercise_finished = False
    lift_right_leg_exercise_finished = False

    message_sent = ''

    def check_correct_pose_timer(self, seconds_treshold):
        if self.correct_pose_time_treshold == None:
            self.correct_pose_time_treshold = time.time()
                
        elif time.time() - self.correct_pose_time_treshold >= seconds_treshold:
            self.correct_pose_time_treshold = None
            return True
        
        return False

    def check_wrong_pose_timer(self, seconds_treshold, block_after):
        if self.wrong_pose_time_treshold == None:
            self.wrong_pose_time_treshold = time.time()
                
        elif time.time() - self.wrong_pose_time_treshold >= seconds_treshold and self.wrong_pose_time_treshold > 0:
            if block_after:
                self.wrong_pose_time_treshold = 0
            # else:
            #     self.correct_pose_time_treshold = None
            return True
        
        return False
    
    def check_base_pose_timer(self, seconds_treshold):
        if self.base_pose_time_treshold == None:
            self.base_pose_time_treshold = time.time()
                
        elif time.time() - self.base_pose_time_treshold >= seconds_treshold and self.base_pose_time_treshold > 0:
            return True
        
        return False

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
            np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
    
    def visual_debug_up(self, image, landmarks):
        pass