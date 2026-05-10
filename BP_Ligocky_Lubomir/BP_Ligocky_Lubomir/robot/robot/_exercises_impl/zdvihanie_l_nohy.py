
import time
import math
import random
import sys
import os


from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'iba_zdvihanie_noh')
if module_path not in sys.path:
    sys.path.append(module_path)

import left_leg_exercise
import right_leg_exercise
import go_back_to_stable_position
import go_back_to_stable_position_pld


class ZvihanieLavejNohy(RobotExerciseUtils):

    def __init__(self, naoqi_instance):
        super(ZvihanieLavejNohy, self).__init__(naoqi_instance)
        self.exercise_name = "left_foot_lifting" #noha'
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get(
            "default", "Začiatok cviku, zdvíhanie nôh")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})

    def run_exercise(self, score, message, conn):
        if message == 'lift_left_leg_start':
            sentence_to_say = self.warning_sentences.get("on_phase", {}).get("lift_left_leg_start", "Prejdiťe na cvik dva, dvíhaňie kolien.")
            self.naoqi.speak_or_message(sentence_to_say)
            self.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

        elif 'lift_left_leg_end' in message:
            self.motionProxy.angleInterpolationBezier(go_back_to_stable_position.names, go_back_to_stable_position.times, go_back_to_stable_position.keys)
            sentence_to_say = self.warning_sentences.get("on_phase", {}).get("lift_left_leg_end",
                                                         "Koniec dvíhaňia kolien na ľavej nohe. Teraz si dáme petnásťsekundovú prestávku.")
            self.naoqi.speak_or_message(sentence_to_say)
            self.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)

        elif message == 'left_leg_down':
            # set center of gravity to right leg
            self.motionProxy.post.angleInterpolation(
                right_leg_exercise.names, right_leg_exercise.keys, right_leg_exercise.times, True)
            
            time.sleep(3.5)

            self.say_score(score, conn)
            time.sleep(1)

            if score < 4:
                sentence_to_say = self.warning_sentences.get("on_phase", {}).get("left_leg_down",
                                                             "Zdvihňite ľavú nohu a pravú ruku upažťe")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = self.warning_sentences.get("on_phase", {}).get("repetition_phase",
                                                             "Zopakujeme znovu")
                self.naoqi.speak_or_message(sentence_to_say)

            jointNames = ["RKneePitch", "RAnklePitch", "RHipPitch", "LShoulderRoll", "LElbowRoll"]
            targetAngles = [
                [1.4],  # RKneePitch, adjusted to approximately 57.3 degrees
                [-0.65],  # RAnklePitch, adjusted to approximately -34.38 degrees
                [-0.8],  # RHipPitch, adjusted to approximately -40.15 degrees
                
                [1.3264502315],  # LShoulderRoll, adjusted to approximately 57.3 degrees
                [1.3264502315]   # LElbowRoll, adjusted to approximately 57.3 degrees
            ]
            times = [[3], [3], [3], [3], [3]]
            self.motionProxy.angleInterpolation(jointNames, targetAngles, times, False)

        elif message == 'left_leg_up':
            time.sleep(0.5)
            self.motionProxy.angleInterpolationBezier(go_back_to_stable_position.names, go_back_to_stable_position.times, go_back_to_stable_position.keys)
            sentence_to_say = self.warning_sentences.get("on_phase", {}).get("left_leg_up",
                                                         "Poľožťe nohu na zem a pravú ruku pripažťe")
            self.naoqi.speak_or_message(sentence_to_say)
