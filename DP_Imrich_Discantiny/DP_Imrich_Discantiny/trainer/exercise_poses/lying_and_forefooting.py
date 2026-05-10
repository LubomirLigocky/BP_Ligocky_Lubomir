import time
import math

from exercise_poses.helper_poses.poses_lying import LyingPose

from exercise_poses.exercise_base import ExerciseBase

class ForefootingLyingPose(ExerciseBase):

    sit_forefooting_in_lying_sent00 = False
    sit_forefooting_in_lying_sent01 = False
    sit_forefooting_in_lying_sent02 = False
    sit_forefooting_in_lying_sent03 = False
    sit_forefooting_in_lying_sent04 = False

    def __init__(self):
        super().__init__()
        self.lying_poses = LyingPose()
        self.curr_exercise_name = "orefooting_in_lying"

        self.wrong_arm = False
        self.wrong_leg = False
    
    def reset_forefooting_in_lying_signal(self):
        self.sit_forefooting_in_lying_sent00 = False
        self.sit_forefooting_in_lying_sent01 = False
        self.sit_forefooting_in_lying_sent02 = False
        self.sit_forefooting_in_lying_sent03 = False
        self.sit_forefooting_in_lying_sent04 = False
    
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
        is_person_lying_init = self.lying_poses.is_person_lying_on_floor_init(landmarks)
        right_leg_lifted = self.lying_poses.is_right_leg_lifted(landmarks)
        left_leg_lifted = self.lying_poses.is_left_leg_lifted(landmarks)

        if self.sit_forefooting_in_lying_sent00 == False:
            if is_person_lying_init is True:
                stage_signal.emit("00,", "forefooting_in_lying_fullfilled", self.camera_exerice_score) # 0. faza - uz lezi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.sit_forefooting_in_lying_sent00 = True

        if right_leg_lifted is True:
            if self.sit_forefooting_in_lying_sent01 == False and self.sit_forefooting_in_lying_sent00 == True:
                stage_signal.emit("01,", "forefooting_in_lying_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                self.sit_forefooting_in_lying_sent01 = True

        if right_leg_lifted is False and is_person_lying_init is True:
            if self.sit_forefooting_in_lying_sent02 == False and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
                stage_signal.emit("02,", "forefooting_in_lying_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihame lavu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                self.sit_forefooting_in_lying_sent02 = True

        if left_leg_lifted is True:
            if self.sit_forefooting_in_lying_sent03 == False and self.sit_forefooting_in_lying_sent02 == True and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
                stage_signal.emit("03,", "forefooting_in_lying_fullfilled", self.camera_exerice_score) # 3. faza - dal aj lavu nohu naspat
                exercise_label_signal.emit("Clovek ma dat dole lavu nohu.")
                self.sit_forefooting_in_lying_sent03 = True

        if left_leg_lifted is False and is_person_lying_init is True:
            if self.sit_forefooting_in_lying_sent04 == False and self.sit_forefooting_in_lying_sent03 == True and self.sit_forefooting_in_lying_sent02 == True and self.sit_forefooting_in_lying_sent01 == True and self.sit_forefooting_in_lying_sent00 == True:
                stage_signal.emit("04,", "forefooting_in_lying_fullfilled", self.camera_exerice_score)
                self.sit_forefooting_in_lying_sent04 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)
                self.reset_forefooting_in_lying_signal()