import time
import math
from exercise_poses.forefooting_exercise import BasicForefootingExercise


class ForefootingRozpazovaniePose(BasicForefootingExercise):

    sit_forefooting_arm_raising_sent00 = False
    sit_forefooting_arm_raising_sent01 = False
    sit_forefooting_arm_raising_sent02 = False
    sit_forefooting_arm_raising_sent03 = False
    sit_forefooting_arm_raising_sent04 = False
    sit_forefooting_arm_raising_sent05 = False
    sit_forefooting_arm_raising_sent06 = False
    sit_forefooting_arm_raising_sent07 = False
    sit_forefooting_arm_raising_sent08 = False

    sit_forefooting_arm_raising_sent00 = False

    def __init__(self):
        super().__init__()
        self.curr_exercise_name = "forefooting_rozpazovanie_exercise"

        self.leg_wrong = False
        self.arm_wrong = False
        
        self.emit_msg_legs = ''
        self.emit_msg_arms = ''
    
    def reset_forefooting_arm_raising_signal(self):
        self.sit_forefooting_arm_raising_sent00 = False
        self.sit_forefooting_arm_raising_sent01 = False
        self.sit_forefooting_arm_raising_sent02 = False
        self.sit_forefooting_arm_raising_sent03 = False
        self.sit_forefooting_arm_raising_sent04 = False
        self.sit_forefooting_arm_raising_sent05 = False
        self.sit_forefooting_arm_raising_sent06 = False
        self.sit_forefooting_arm_raising_sent07 = False
        self.sit_forefooting_arm_raising_sent08 = False
    
    
    def do_check_exercise(self, landmarks, stage_signal, exercise_label_signal, score_signal):
        hands_raised_in_sitting = self.sit_poses.is_hands_raised_in_sitting(landmarks)
        is_person_sitting = self.sit_poses.is_person_sitting(landmarks)
        is_right_leg_raised = self.legs_poses.is_right_leg_raised(landmarks)
        is_left_leg_raised = self.legs_poses.is_left_leg_raised(landmarks)

        if self.sit_forefooting_arm_raising_sent00 == False:
            if is_person_sitting is True:
                stage_signal.emit("00,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score) # 0. faza - uz sedi, zdvihneme mu pravu nohu
                exercise_label_signal.emit("Clovek ma zdvihnut pravu nohu.")
                self.sit_forefooting_arm_raising_sent00 = True

        if True:
            if is_right_leg_raised is True and hands_raised_in_sitting is False:
                if self.sit_forefooting_arm_raising_sent01 == False and self.sit_forefooting_arm_raising_sent00 == True:
                    stage_signal.emit("01,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score) # 1. faza - uz ju zdvihol, dame ju naspat
                    exercise_label_signal.emit("Clovek ma vratit pravu nohu naspat na zem.")
                    self.sit_forefooting_arm_raising_sent01 = True

            if is_left_leg_raised is False and is_right_leg_raised is False and hands_raised_in_sitting is False and is_person_sitting is True:
                if self.sit_forefooting_arm_raising_sent02 == False and self.sit_forefooting_arm_raising_sent01 == True and self.sit_forefooting_arm_raising_sent00 == True:
                    stage_signal.emit("02,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score) # 2. faza - uz ju dal naspat, zdvihneme ruky nad hlavu
                    exercise_label_signal.emit("Clovek ma zdvihnut ruky nad hlavu.")
                    self.sit_forefooting_arm_raising_sent02 = True

            if is_left_leg_raised is False and is_right_leg_raised is False and hands_raised_in_sitting is True:
                if self.sit_forefooting_arm_raising_sent03 == False and self.sit_forefooting_arm_raising_sent02 == True and self.sit_forefooting_arm_raising_sent01 == True and self.sit_forefooting_arm_raising_sent00 == True:
                    stage_signal.emit("03,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score) # 3. faza - uz ich zdvihol nad hlavu, davame ich naspat
                    exercise_label_signal.emit("Clovek ma dat dole ruky.")
                    self.sit_forefooting_arm_raising_sent03 = True

            if is_left_leg_raised is False and hands_raised_in_sitting is False:
                if self.sit_forefooting_arm_raising_sent04 == False and self.sit_forefooting_arm_raising_sent03 == True and self.sit_forefooting_arm_raising_sent02 == True and self.sit_forefooting_arm_raising_sent01 == True and self.sit_forefooting_arm_raising_sent00 == True:
                    stage_signal.emit("04,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score) # 4. faza - uz ju zdvihol, dame ju naspat
                    exercise_label_signal.emit("Clovek ma zdvihnut lavu nohu.")
                    self.sit_forefooting_arm_raising_sent04 = True

            if is_left_leg_raised is True and hands_raised_in_sitting is False:
                if self.sit_forefooting_arm_raising_sent05 == False and self.sit_forefooting_arm_raising_sent04 == True:
                    stage_signal.emit("05,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score)
                    exercise_label_signal.emit("Clovek ma lavu nohu naspat")
                    self.sit_forefooting_arm_raising_sent05 = True

            if is_left_leg_raised is False and is_right_leg_raised is False and hands_raised_in_sitting is False:
                if self.sit_forefooting_arm_raising_sent06 == False and self.sit_forefooting_arm_raising_sent05 == True:
                    stage_signal.emit("06,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score)
                    exercise_label_signal.emit("Clovek ma zdvihnut ruky.")
                    self.sit_forefooting_arm_raising_sent06 = True

            if is_left_leg_raised is False and hands_raised_in_sitting is True:
                if self.sit_forefooting_arm_raising_sent07 == False and self.sit_forefooting_arm_raising_sent06 == True:
                    stage_signal.emit("07,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score)
                    exercise_label_signal.emit("Clovek ma dat ruky naspat.")
                    self.sit_forefooting_arm_raising_sent07 = True

            if is_left_leg_raised is False and hands_raised_in_sitting is False:
                if self.sit_forefooting_arm_raising_sent08 == False and self.sit_forefooting_arm_raising_sent07 == True:
                    stage_signal.emit("08,", "forefooting_arm_raising_fullfilled", self.camera_exerice_score)
                    exercise_label_signal.emit("Clovek ma dat ruky naspat.")
                    self.sit_forefooting_arm_raising_sent08 = True

                    self.camera_exerice_score += 1
                    score_signal.emit(True)
                    self.reset_forefooting_arm_raising_signal()