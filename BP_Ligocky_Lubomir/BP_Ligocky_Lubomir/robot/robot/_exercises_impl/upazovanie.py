# -*- coding: utf-8 -*-

import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sit_exercise

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)


class Upazovanie(RobotExerciseUtils):
    
      
    def __init__(self, naoqi_instance):
        super(Upazovanie, self).__init__(naoqi_instance)
        self.exercise_name = 'tpose'
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get("default","Začiatok cviku, upažovanie")
        #self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default", "Super. Zvládľi sme to na jednotku.")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})

    def warning_say(self, message):

        """if 'Base_pos_back' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos_back", "Prosím pripaž ruky")
            self.naoqi.speak_or_message(sentence_to_say)
            
        elif 'Base_pos' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos", "Prosím upaž ruky")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "tpose_arms_above" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("tpose_arms_above",
                                                                               "Posuň upažené ruky nižšie na vodorovnu polohu.")
            self.naoqi.speak_or_message(sentence_to_say)
               
        elif "tpose_arms_below" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("tpose_arms_below",
                                                                               "Posuň upažené ruky vyššie na vodorovnu polohu.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "tpose_arms_wrong" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("tpose_arms_wrong",
                                                                               "Skús upažiť ruky vodorovne.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Foreground_hands_pos" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("tpose_arms_wrong",
                                                                               "Vystri ruky vodorovne na strany, a nie do predu.")
            self.naoqi.speak_or_message(sentence_to_say)"""

    def run_exercise(self, score, message, conn):
        if message == 'tpose_down':

            # if uz_zdvihol_hlavu is False:
            #     # zdvihni_hlavu()
            #     uz_zdvihol_hlavu = True
                
            self.say_score(score, conn)
           
            if self.naoqi.is_physical is True:
                time.sleep(0.5)
            else:
                time.sleep(1)

            if score == 9:
                phase1_sentence = self.exercise_speach_lang.get("on_phase", {}).get("last", "Posledný krát")
                self.naoqi.speak_or_message(phase1_sentence)
            else:
                phase1_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase1", "Upaž ruky")
                self.naoqi.speak_or_message(phase1_sentence)
            
            time.sleep(0.5)


            # Adjustment of arms position (Up)
            self.naoqi.motionProxy.setAngles(["LShoulderRoll"], 1.3264502315, 0.3)
            self.naoqi.motionProxy.setAngles(["LElbowRoll"], 1.3264502315, 0.3)

            self.naoqi.motionProxy.setAngles(["RShoulderRoll"], -1.3264502315, 0.3)
            self.naoqi.motionProxy.setAngles(["RElbowRoll"], -1.3264502315, 0.3)
            if self.naoqi.is_physical is True:
                time.sleep(1)
            else:
                time.sleep(0.5)
            
            conn.send("ExerciseContinue_tposeE".encode())  
            
            print(score)

        elif message == 'tpose_up':

            if self.naoqi.is_physical is True:
                time.sleep(0.75)
            else:
                time.sleep(0.5)
            phase2_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase2", "Pripaž ruky")
            if score < 3:
                self.naoqi.speak_or_message(phase2_sentence)
                # speechProxy.post.say(str("Pripažťe"))
            else:
                self.naoqi.speak_or_message(phase2_sentence)
                # speechProxy.post.say(str("Pripažťe"))

            time.sleep(0.5)
            # Adjustment of arms position (Down)
            self.naoqi.motionProxy.setAngles(["LShoulderRoll"], 0.0, 0.3)
            self.naoqi.motionProxy.setAngles(["LElbowRoll"], 0.0, 0.3)

            self.naoqi.motionProxy.setAngles(["RShoulderRoll"], 0.0, 0.3)
            self.naoqi.motionProxy.setAngles(["RElbowRoll"], 0.0, 0.3)
            if self.naoqi.is_physical is True:
                time.sleep(0.75)
            else:
                time.sleep(0.25)

            conn.send("ExerciseContinue_tposeE".encode())
        
        elif message == 'tpose_start':
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            self.naoqi.speak_or_message(self.starting_sentence)
            conn.send("ExerciseContinue_tposeE".encode())

        elif message == 'tpose_end':
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

            self.naoqi.speak_or_message(self.ending_sentence)