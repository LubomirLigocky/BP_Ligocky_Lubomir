import time
import math

from exercise_poses.helper_poses.poses_sit import SitPose

from exercise_poses.exercise_base import ExerciseBase

import mediapipe as mp


class SadanieNaStolickuPose(ExerciseBase):

    sit_stand_raise_arms_sent00 = False # Initial
    sit_stand_raise_arms_sent01 = False # person is sitting but did't have arms above head nor was standing before
    sit_stand_raise_arms_sent02 = False # a person is standing NOT above the head
    sit_stand_raise_arms_sent03 = False # A PERSON IS STANDING WITH ARMS ABOVE head
    sit_stand_raise_arms_sent04 = False # a person is sitting and HAD hands above before
    sit_stand_raise_arms_sent05 = False # a person is sitting and HAD hands above before
    
    def __init__(self):
        super().__init__()
        self.sit_poses = SitPose()
        self.curr_exercise_name = "sadanie_na_stolicku_exercise"
    
    def reset_stand_raise_arms_signal(self):
        self.sit_stand_raise_arms_sent00 = False
        self.sit_stand_raise_arms_sent01 = False
        self.sit_stand_raise_arms_sent02 = False
        self.sit_stand_raise_arms_sent03 = False
        self.sit_stand_raise_arms_sent04 = False
        self.sit_stand_raise_arms_sent05 = False

    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_person_standing = self.sit_poses.is_person_standing(landmarks)

        if self.sit_stand_raise_arms_sent00 == False:
            stage_signal.emit("00,", "sadanie_na_stolicku_fullfilled", self.camera_exerice_score) # 0. faza - chceme ho dat to vychodzej polohy - signal 00 znaci, aby si sadol
            exercise_label_signal.emit("Zaciatocna pozicia - clovek si ma teraz sadnut.")
            self.sit_stand_raise_arms_sent00 = True

        # Robot cloveku ukazal v 00, aby si sadol, teraz cakame, kym si clovek sadne - cakame, kym in_person_standing bude False
        if (is_person_standing is False) and (is_person_sitting is True):
            if self.sit_stand_raise_arms_sent01 == False and self.sit_stand_raise_arms_sent00 == True:
                stage_signal.emit("01,", "sadanie_na_stolicku_fullfilled", self.camera_exerice_score)
                exercise_label_signal.emit("Clovek si uz sadol. Mozeme pokr. dalej.")
                self.sit_stand_raise_arms_sent01 = True

        # Robot vstal, cakame, kym clovek vstane a ruky este nema nad hlavou
        if (is_person_standing is True) and (self.arms_poses.check_arms_raised_up(landmarks) is False):
            if self.sit_stand_raise_arms_sent02 == False and self.sit_stand_raise_arms_sent01 == True and self.sit_stand_raise_arms_sent00 == True:
                stage_signal.emit("02,", "sadanie_na_stolicku_fullfilled", self.camera_exerice_score)
                exercise_label_signal.emit("Clovek sa postavil a ruky ma pri tele.")
                self.sit_stand_raise_arms_sent02 = True

                self.camera_exerice_score += 1
                score_signal.emit(True)

                self.reset_stand_raise_arms_signal()