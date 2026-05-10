import time
import math

from exercise_poses.helper_poses.poses_arms import ArmsPose
from exercise_poses.helper_poses.poses_legs import LegsPose
from exercise_poses.helper_poses.poses_sit import SitPose
from exercise_poses.exercise_base import ExerciseBase


class BasicForefootingExercise(ExerciseBase):
    sit_forefooting_on_chair_sent00 = False
    sit_forefooting_on_chair_sent01 = False
    sit_forefooting_on_chair_sent02 = False
    sit_forefooting_on_chair_sent03 = False
    sit_forefooting_on_chair_sent04 = False

    def __init__(self):
        self.arms_poses = ArmsPose()
        self.legs_poses = LegsPose()
        self.sit_poses = SitPose()


    def reset_forefooting_on_chair_signal(self):
        self.sit_forefooting_on_chair_sent00 = False
        self.sit_forefooting_on_chair_sent01 = False
        self.sit_forefooting_on_chair_sent02 = False
        self.sit_forefooting_on_chair_sent03 = False
        self.sit_forefooting_on_chair_sent04 = False
   

class ForefootingRukyPriTelePose(BasicForefootingExercise):
    def __init__(self):
        super().__init__()
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
        
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_right_leg_raised = self.legs_poses.is_right_leg_raised(landmarks)
        is_left_leg_rised = self.legs_poses.is_left_leg_raised(landmarks)


        if self.sit_forefooting_on_chair_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_ruky_pri_tele_fullfilled", self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.sit_forefooting_on_chair_sent00 = True
        
        if is_right_leg_raised is True and is_left_leg_rised is False:
            if self.sit_forefooting_on_chair_sent01 == False and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("01,", "forefooting_ruky_pri_tele_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                self.sit_forefooting_on_chair_sent01 = True

        if is_right_leg_raised is False and is_left_leg_rised is False:
            if self.sit_forefooting_on_chair_sent02 == False and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("02,", "forefooting_ruky_pri_tele_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_on_chair_sent02 = True

        if is_left_leg_rised is True and is_right_leg_raised is False:
            if self.sit_forefooting_on_chair_sent03 == False and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("03,", "forefooting_ruky_pri_tele_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                self.sit_forefooting_on_chair_sent03 = True

        if is_left_leg_rised is False and is_right_leg_raised is False:
            if self.sit_forefooting_on_chair_sent04 == False and self.sit_forefooting_on_chair_sent03 == True and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("04,", "forefooting_ruky_pri_tele_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_on_chair_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_on_chair_signal()
   

class ForefootingRukyNadHlavuPose(BasicForefootingExercise):
    def __init__(self):
        super().__init__()
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
       
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_right_leg_raised = self.legs_poses.is_right_leg_raised(landmarks)
        is_left_leg_rised = self.legs_poses.is_left_leg_raised(landmarks)
        arms_raised_above_head = self.is_hands_raised_in_sitting(landmarks)

        print(arms_raised_above_head)

        if self.sit_forefooting_on_chair_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_ruky_nad_hlavu_fullfilled", self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.sit_forefooting_on_chair_sent00 = True
        
        if is_right_leg_raised is True and arms_raised_above_head is True:
            if self.sit_forefooting_on_chair_sent01 == False and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("01,", "forefooting_ruky_nad_hlavu_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                self.sit_forefooting_on_chair_sent01 = True

        if is_right_leg_raised is False and arms_raised_above_head is False:
            if self.sit_forefooting_on_chair_sent02 == False and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("02,", "forefooting_ruky_nad_hlavu_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_on_chair_sent02 = True

        if is_left_leg_rised is True and arms_raised_above_head is True:
            if self.sit_forefooting_on_chair_sent03 == False and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("03,", "forefooting_ruky_nad_hlavu_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                self.sit_forefooting_on_chair_sent03 = True

        if is_left_leg_rised is False and arms_raised_above_head is False:
            if self.sit_forefooting_on_chair_sent04 == False and self.sit_forefooting_on_chair_sent03 == True and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("04,", "forefooting_ruky_nad_hlavu_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_on_chair_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_on_chair_signal()



class ForefootingRukyOnChairPose(BasicForefootingExercise):
    def __init__(self):
       super().__init__()
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
       
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_right_leg_raised = self.legs_poses.is_right_leg_raised(landmarks)
        is_left_leg_rised = self.legs_poses.is_left_leg_raised(landmarks)

        if self.sit_forefooting_on_chair_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_on_chair_fullfilled", self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.sit_forefooting_on_chair_sent00 = True
        
        if is_right_leg_raised is True:
            if self.sit_forefooting_on_chair_sent01 == False and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("01,", "forefooting_on_chair_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                self.sit_forefooting_on_chair_sent01 = True

        if is_right_leg_raised is False:
            if self.sit_forefooting_on_chair_sent02 == False and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("02,", "forefooting_on_chair_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_on_chair_sent02 = True

        if is_left_leg_rised is True:
            if self.sit_forefooting_on_chair_sent03 == False and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("03,", "forefooting_on_chair_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                self.sit_forefooting_on_chair_sent03 = True

        if is_left_leg_rised is False:
            if self.sit_forefooting_on_chair_sent04 == False and self.sit_forefooting_on_chair_sent03 == True and self.sit_forefooting_on_chair_sent02 == True and self.sit_forefooting_on_chair_sent01 == True and self.sit_forefooting_on_chair_sent00 == True:
                stage_signal.emit("04,", "forefooting_on_chair_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_on_chair_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_on_chair_signal()