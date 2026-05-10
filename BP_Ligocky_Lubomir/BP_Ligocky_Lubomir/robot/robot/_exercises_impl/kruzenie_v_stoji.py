# -*- coding: utf-8 -*-

import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'kruzenie')
if module_path not in sys.path:
    sys.path.append(module_path)

import ruky_v_stoji_dole

import ruky_v_stoji_hore


class KruzenieVStoji(RobotExerciseUtils):
    is_ending = False

    def __init__(self, naoqi_instance):
        super(KruzenieVStoji, self).__init__(naoqi_instance)

        self.exercise_name = "arm_circling_in_standing" #"arm_circling"
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get(
            "default", "Začíname cvičiť krúženie rukami v stoji, opakuj po mňe")
        self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default",
                                                                               "Super. Zvládľi sme to na jednotku.")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})

    def run_exercise(self, score, message, conn):
        
        if message == "arm_circling_start":
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            self.naoqi.speak_or_message(self.starting_sentence)
            conn.send("ExerciseContinue_kr".encode())

        elif message == "arm_circling_end":
            self.is_ending = True

            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            self.naoqi.speak_or_message(self.ending_sentence)
        
        elif message == "arm_circling_down":
            sentence_to_say = self.exercise_speach_lang.get("on_phase", {}).get("arm_circling_down", "Otoč ruky dole")
            self.naoqi.speak_or_message(sentence_to_say)

            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_stoji_dole.names, ruky_v_stoji_dole.times, ruky_v_stoji_dole.keys)
            
            time.sleep(0.5)
            conn.send("ExerciseContinue_kr".encode())
        
        elif message == "arm_circling_up" and self.is_ending is False:
            self.say_score(score, conn)
            sentence_to_say = self.exercise_speach_lang.get("on_phase", {}).get("arm_circling_up", "Vzpaž ruky nad hlavu")
            self.naoqi.speak_or_message(sentence_to_say)

            self.naoqi.motionProxy.angleInterpolationBezier(ruky_v_stoji_hore.names, ruky_v_stoji_hore.times, ruky_v_stoji_hore.keys)

            conn.send("ExerciseContinue_kr".encode())
    
    def warning_say(self, message):
        if "ZLE_hore" in message:
            sentence_to_say = self.warning_sentences.get("ZLE_hore", "Nemáš vystrete ruky nad hlavou.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Base_hore" in message:
            sentence_to_say = self.warning_sentences.get("Base_hore", "Prosím vpaž ruky hore.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "ZLE_dole" in message:
            sentence_to_say = self.warning_sentences.get("ZLE_dole", "Polož ruky dole.")
            self.naoqi.speak_or_message(sentence_to_say)
