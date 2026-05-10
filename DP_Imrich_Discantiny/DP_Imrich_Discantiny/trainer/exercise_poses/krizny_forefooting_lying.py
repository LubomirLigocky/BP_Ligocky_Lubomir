
import time
import math

from exercise_poses.helper_poses.poses_lying import LyingPose

from exercise_poses.exercise_base import ExerciseBase

class KriznyForefootingLyingPose(ExerciseBase):
    
    sit_forefooting_in_lying_sent00 = False
    sit_forefooting_in_lying_sent01 = False
    sit_forefooting_in_lying_sent02 = False
    sit_forefooting_in_lying_sent03 = False
    sit_forefooting_in_lying_sent04 = False

    def __init__(self):
        super().__init__()
        self.lying_poses = LyingPose()
        self.curr_exercise_name = "krizny_forefooting_in_lying"

        self.wrong_pose_msg = ''
        self.message_sent = ''
    
    def reset_forefooting_in_lying_signal(self):
        self.sit_forefooting_in_lying_sent00 = False
        self.sit_forefooting_in_lying_sent01 = False
        self.sit_forefooting_in_lying_sent02 = False
        self.sit_forefooting_in_lying_sent03 = False
        self.sit_forefooting_in_lying_sent04 = False
    
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal, depth):
        is_person_lying_init = self.lying_poses.is_person_lying_on_floor_init(landmarks)

        right_leg_lifted, lift_leg1 = self.lying_poses.is_right_leg_lifted(landmarks)
        left_leg_lifted, lift_leg2= self.lying_poses.is_left_leg_lifted(landmarks)

        is_right_arm_lifted_when_lying, lift_arm1 = self.lying_poses.is_right_arm_lifted_when_lying(landmarks)
        is_left_arm_lifted_when_lying, lift_arm2 = self.lying_poses.is_left_arm_lifted_when_lying(landmarks)

        if self.sit_forefooting_in_lying_sent00 == False:
            if is_person_lying_init is True:
                stage_signal.emit("00,", "krizny_forefooting_in_lying_fullfilled", self.camera_exerice_score) # 0. faza - uz lezi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                
                self.wrong_pose_time_treshold = None
                self.sit_forefooting_in_lying_sent00 = True
                self.exercise_lock = True
            else:
              
                # stage_signal.emit("warning", "Not_lying", self.camera_exerice_score)
                exercise_label_signal.emit("Nelezi.")
                    
        if self.sit_forefooting_in_lying_sent01 == False and self.sit_forefooting_in_lying_sent00 == True:
          
            
            if right_leg_lifted is True and is_left_arm_lifted_when_lying is True:
                print(right_leg_lifted, is_left_arm_lifted_when_lying, is_person_lying_init)
                self.wrong_pose_time_treshold = None
                self.base_pose_time_treshold = None
                
                if self.check_correct_pose_timer(0.5):
                    stage_signal.emit("01,", "krizny_forefooting_in_lying_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                    exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                    self.sit_forefooting_in_lying_sent01 = True
                    self.exercise_lock = True

            elif is_person_lying_init:
                self.correct_pose_time_treshold = None
                self.base_pose_time_treshold = None

                if self.check_base_pose_timer(3.5):
                    stage_signal.emit("warning", "base_pose_1")
                    self.exercise_lock = True
                    self.wrong_pose_time_treshold = 0
            else:
                self.correct_pose_time_treshold = None
                self.base_pose_time_treshold = None

                if left_leg_lifted is True and is_right_arm_lifted_when_lying is True:
                
                    self.wrong_pose_msg = "reverse_pose,"
                
                elif (left_leg_lifted is True or is_right_arm_lifted_when_lying is True):
                    if (right_leg_lifted is True and left_leg_lifted is True) or (is_left_arm_lifted_when_lying is True and is_right_arm_lifted_when_lying is True):
                        self.wrong_pose_msg = 'wrong_pose,'
                    else:
                        self.wrong_pose_msg = 'wrong_lift'
                
                elif (right_leg_lifted is False or is_left_arm_lifted_when_lying is False): 
                    
                    if right_leg_lifted is False and is_left_arm_lifted_when_lying is True:
                        if lift_leg1 == 1:
                            self.wrong_pose_msg = 'Iba_prava_noha_nizko'
                    elif right_leg_lifted is True and is_left_arm_lifted_when_lying is False:
                        if lift_arm2 == 1:
                            self.wrong_pose_msg = 'Iba_lava_ruka_nizko'
                    elif right_leg_lifted is False and is_left_arm_lifted_when_lying is False:
                        if lift_leg1 == 1 and lift_arm2 == 1:
                            self.wrong_pose_msg = 'Ruka_a_noha_nizko'
        
                if self.wrong_pose_msg  != self.message_sent:

                    if self.check_wrong_pose_timer(2.0, False):
                        
                        self.message_sent = self.wrong_pose_msg
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        exercise_label_signal.emit(self.message_sent)
                        self.exercise_lock = True
                        
                        self.wrong_pose_time_treshold = None
                  

        if self.sit_forefooting_in_lying_sent02 == False and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
            if right_leg_lifted is False and is_person_lying_init is True:
                stage_signal.emit("02,", "krizny_forefooting_in_lying_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_in_lying_sent02 = True
                self.exercise_lock = True

        if self.sit_forefooting_in_lying_sent03 == False and self.sit_forefooting_in_lying_sent02 == True and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
           

            if left_leg_lifted is True and is_right_arm_lifted_when_lying is True:
                self.wrong_pose_time_treshold = None
                self.base_pose_time_treshold = None

                if self.check_correct_pose_timer(0.5):
                    stage_signal.emit("03,", "krizny_forefooting_in_lying_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                    exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                    self.sit_forefooting_in_lying_sent03 = True
                    self.exercise_lock = True
           
            elif is_person_lying_init:
                self.correct_pose_time_treshold = None
                self.base_pose_time_treshold = None
                
                if self.check_base_pose_timer(3.5):
                    stage_signal.emit("warning", "base_pose_2")
                    self.exercise_lock = True
                    self.wrong_pose_time_treshold = 0

            else:
                self.correct_pose_time_treshold = None
                self.base_pose_time_treshold = None

                if right_leg_lifted is True and is_left_arm_lifted_when_lying is True:
                    self.wrong_pose_msg = "reverse_pose,"
                
                elif right_leg_lifted is True or is_left_arm_lifted_when_lying is True:
                    if (right_leg_lifted is True and left_leg_lifted is True) or (is_left_arm_lifted_when_lying is True and is_right_arm_lifted_when_lying is True):
                        self.wrong_pose_msg = 'wrong_pose,'
                    else:
                        self.wrong_pose_msg = 'wrong_lift'
                
                elif left_leg_lifted is False or is_right_arm_lifted_when_lying is False: 
                    
                    if left_leg_lifted is False and is_right_arm_lifted_when_lying is True:
                        if lift_leg2 == 1:
                            self.wrong_pose_msg = 'Iba_lava_noha_nizko'
                       
                    elif left_leg_lifted is True and is_right_arm_lifted_when_lying is False:
                        if lift_arm1 == 1:
                            self.wrong_pose_msg = 'Iba_prava_ruka_nizko'
                        
                    elif left_leg_lifted is False and is_right_arm_lifted_when_lying is False:
                        if lift_leg2 == 1 and lift_arm1 == 1:
                            self.wrong_pose_msg = 'Ruka_a_noha_nizko'

            
                if self.wrong_pose_msg  != self.message_sent:

                    if self.check_wrong_pose_timer(2.0, False):
                
                        self.message_sent = self.wrong_pose_msg
                        stage_signal.emit("warning", self.message_sent, self.camera_exerice_score)
                        exercise_label_signal.emit(self.message_sent)
                        self.exercise_lock = True
                        
                        self.wrong_pose_time_treshold = None
                       

        if self.sit_forefooting_in_lying_sent04 == False and self.sit_forefooting_in_lying_sent03 == True and self.sit_forefooting_in_lying_sent02 == True and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
            if left_leg_lifted is False and is_person_lying_init is True:
                stage_signal.emit("04,", "krizny_forefooting_in_lying_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_in_lying_sent04 = True

                self.exercise_lock = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_in_lying_signal()