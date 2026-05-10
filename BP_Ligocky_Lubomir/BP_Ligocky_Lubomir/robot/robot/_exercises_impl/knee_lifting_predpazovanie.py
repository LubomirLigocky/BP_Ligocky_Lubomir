# -*- coding: utf-8 -*-
import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import stand_up_from_chair
import sitting_position_for_extending_legs as sit_on_chair
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu

module_path = os.path.join(os.getcwd(), 'rozpazovanie_nohy_ruky_knee_lifting')
if module_path not in sys.path:
    sys.path.append(module_path)

# Predpazovanie prava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy_knee_lifting as ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy
import predpazovanie_a_zdvihanie_pravej_nohy_sucasne2_knee_lifting as predpazovanie_a_zdvihanie_pravej_nohy_sucasne2

# Predpazovanie lava noha
import daj_ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy_knee_lifting as ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy
import predpazovanie_a_zdvihanie_lavej_nohy_sucasne_knee_lifting as predpazovanie_a_zdvihanie_lavej_nohy_sucasne


class KneeLiftingPredpazovanie(RobotExerciseUtils):

    def __init__(self, naoqi_instance):
        super(KneeLiftingPredpazovanie, self).__init__(naoqi_instance)
        self.exercise_name = "knee_lifting_predpazovanie"
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get(
            "default", "Začíname zdvíhať kolená na stoličke s upažovaňím. Sadňi si na stoličku.")
        self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default",
                                                                               "Koniec cvičenia, Pripravíme sa na ďalší cvik.")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})
        self.say_emotion_after_end = False
        self.is_sitting = True

        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        self.naoqi.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def reset(self):
        self.finished_phases = {"0": False, "1": False, "2": False, "3": False, "4": False}

    def start_forefooting(self):
        self.naoqi.motionProxy.setFallManagerEnabled(False)
        sit_on_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in sit_on_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(sit_on_chair.names, sit_on_chair_times, sit_on_chair.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names,
                                                        ruky_k_telu_zo_zakladneho_sedu.times,
                                                        ruky_k_telu_zo_zakladneho_sedu.keys)
        #self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_zo_zakladneho_sedu.names, ruky_k_telu_zo_zakladneho_sedu.times, ruky_k_telu_zo_zakladneho_sedu.keys)
        #self.naoqi.motionProxy.setFallManagerEnabled(True)

    def end_forefooting(self):
        stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
        self.naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)
        self.naoqi.motionProxy.setFallManagerEnabled(True)
        self.reset()

    def say_forefooting_emotion(self, message):
        if "start" in message:
            self.say_emotion_start(message, self.starting_sentence)
            self.start_forefooting()
        elif "end" in message:
            self.say_emotion_end(message)
            self.end_forefooting()

    def run_exercise(self, score, message, pending_messages, phase, conn):
        message = message.strip(",")
        print(message)
        print(self.finished_phases["0"])
        print(phase)
        if message == 'knee_lifting_predpazovanie_start':
            if score == 0:
                self.reset()
            self.naoqi.speak_or_message(self.starting_sentence)
            self.start_forefooting()
            conn.send(("ExerciseContinue_" + self.exercise_name).encode())

            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases)

        if message == 'knee_lifting_predpazovanie_en':
            self.naoqi.speak_or_message("Koniec cvičenia, Pripravíme sa na ďalší cvik.")
            self.end_forefooting()
            conn.send(("ExerciseContinue_" + self.exercise_name).encode())

            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

        if message == 'knee_lifting_predpazovanie':
            if phase == 0 and self.finished_phases["0"] == False:  # We put robot to sit first, so we do it in start
                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_lavej_nohy_sucasne.names,
                                                                    predpazovanie_a_zdvihanie_lavej_nohy_sucasne.times,
                                                                    predpazovanie_a_zdvihanie_lavej_nohy_sucasne.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.names,
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.times,
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 1 and self.finished_phases["1"] == False and self.finished_phases["0"] == True:
                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.names,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.times,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.names,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.times,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:
                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.names,
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.times,
                        predpazovanie_a_zdvihanie_pravej_nohy_sucasne2.keys)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(predpazovanie_a_zdvihanie_lavej_nohy_sucasne.names,
                                                                    predpazovanie_a_zdvihanie_lavej_nohy_sucasne.times,
                                                                    predpazovanie_a_zdvihanie_lavej_nohy_sucasne.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 3 and self.finished_phases["3"] == False and self.finished_phases["2"] == True:
                self.finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, self.finished_phases)

                if self.MIRRORING is True:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.names,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.times,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_p_nohy.keys)
                    import time
                    time.sleep(0.5)
                else:
                    self.naoqi.motionProxy.angleInterpolationBezier(ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.names,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.times,
                                                                    ruky_k_telu_z_predpazenia_a_zdvihnutej_l_nohy.keys)

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

            elif phase == 4 and self.finished_phases["4"] == False and self.finished_phases["3"] == True:
                self.finished_phases["4"] = True
                self.remove_items_by_value(pending_messages, score, 4, self.finished_phases, False)

                self.say_score(score + 1, conn)

                self.finished_phases = {str(i): False for i in range(6)}

                conn.send(("ExerciseContinue_" + self.exercise_name + str(phase)).encode())

    def warning_say(self, message):
        leg_wrong = False

        if "knee_liftingPred_a_zdvihni_pravu_nohu" in message:
            sentence_to_say = self.warning_sentences.get(
                "knee_liftingPred_a_zdvihni_pravu_nohu", "Zdvihniťe pravé koleno.")
            self.naoqi.speak_or_message(sentence_to_say)
            leg_wrong = True
            
        if "knee_liftingPred_a_zdvihni_lavu_nohu" in message:
            sentence_to_say = self.warning_sentences.get(
                "knee_liftingPred_a_zdvihni_lavu_nohu", "Zdvihniťe ľavé koleno.")
            self.naoqi.speak_or_message(sentence_to_say)
            leg_wrong = True

        if "In_Base_pos_left" in message:
            sentence_to_say = self.warning_sentences.get(
                "In_Base_pos_left", "Predpažťe ruky a zdvihniťe ľavé koleno")
            self.naoqi.speak_or_message(sentence_to_say)
            return
        
        elif "In_Base_pos_right" in message:
            sentence_to_say = self.warning_sentences.get(
                "In_Base_pos_right", "Predpažťe ruky a zdvihniťe pravé koleno.")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        # - predpazenie
        elif "Predpazene_ruky_vysoko_a_odseba" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_vysoko_a_odseba", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom posuň ruky nižšie na vodorovnu polohu a bližšie k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Posuň ruky nižšie na vodorovnu polohu a bližšie k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_vysoko_a_nespravne" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_vysoko_a_nespravne", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom daj ruky nižšie na vodorovnú pozíciu a do správnej polohy.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Daj ruky nižšie na vodorovnu polohu a do správnej polohy.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_vysoko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_vysoko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň skús ruky posuň nižšie na vodorovnú polohu.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Skús ruky posuň nižšie na vodorovnú polohu.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_nizko_a_odseba" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_nizko_a_odseba", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň skús ruky posuň vyššie na vodorovnú polohu a priblížiť ich bližšie k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Skús ruky posuň vyššie na vodorovnú polohu a priblížiť ich k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_nizko_a_nespravne" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_nizko_a_nespravne", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Tiež daj ruky vyššie na vodorovnú polohu a do správnej polohy.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Daj ruky vyššie na vodorovnú polohu a do správnej polohy.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_nizko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_nizko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň daj ruky vyššie na vodorovnú pozíciu a do správnej polohy.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Skúste ruky posunúť vyššie na vodorovnú polohu.")
                self.naoqi.speak_or_message(sentence_to_say)

         # Iné       
        elif "Predpazene_ruky_priliz_od_seba" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_priliz_od_seba", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Tiež priblíž ruky trochu bližšie k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Priblíž ruky trochu bližšie k sebe.")
                self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Predpazene_ruky_zle" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "both_hands", {}).get("Predpazene_ruky_zle", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Tiež predpaž ruky na vodorovnú polohu.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Predpaž ruky na vodorovnú polohu.")
                self.naoqi.speak_or_message(sentence_to_say)
            
        # Hlášky pre pravú ruku - predpazenie
        elif "Prava_ruka_vysoko_a_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "right_hand", {}).get("Prava_ruka_vysoko_a_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom pravú ruku daj o trošku nižšie a bližšie k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Pravú ruku daj trošku nižšie a bližšie k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_vysoko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "right_hand", {}).get("Prava_ruka_vysoko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom pravú ruku skúste dať o trochu nižšie.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Pravú ruku skúste dať o trochu nižšie.")
                self.naoqi.speak_or_message(sentence_to_say)
               
        elif "Prava_ruka_nizko_a_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "right_hand", {}).get("Prava_ruka_nizko_a_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom pravú ruku zdvihňi trochu vyššie a bližšie k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Pravú ruku zdvihňi trochu vyššie a bližšie k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_nizko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "right_hand", {}).get("Prava_ruka_nizko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň daj pravú ruku trošku vyššie.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Dajťe pravú ruku trošku vyššie.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "right_hand", {}).get("Prava_ruka_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň pravú ruku priblíž viac k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Pravú ruku priblíž viac k ľavej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        # Hlášky pre ľavú ruku - predpazenie
        elif "Lava_ruka_vysoko_a_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "left_hand", {}).get("Lava_ruka_vysoko_a_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom ľavú ruku daj o trošku nižšie a bližšie k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Ľavú ruku daj trošku nižšie a bližšie k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_vysoko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "left_hand", {}).get("Lava_ruka_vysoko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom ľavú ruku skús dať o trochu nižšie.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Ľavú ruku skús dať o trochu nižšie.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_nizko_a_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "left_hand", {}).get("Lava_ruka_nizko_a_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Potom ľavú ruku zdvihňi o trochu vyššie a bližšie k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Ľavú ruku zdvihňi trochu vyššie a bližšie k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_nizko" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "left_hand", {}).get("Lava_ruka_nizko", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň zdvihňi ľavú ruku trošku vyššie.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Zdvihnite ľavú ruku trošku vyššie.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_od_tela" in message:
            naoqi_speech_options = self.warning_sentences.get(
                "left_hand", {}).get("Lava_ruka_od_tela", {})
            if leg_wrong is True:
                time.sleep(0.2)
                sentence_to_say = naoqi_speech_options.get(
                    "leg_wrong", "Zároveň ľavú ruku priblíž viac k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)
            else:
                sentence_to_say = naoqi_speech_options.get(
                    "leg_right", "Ľavú ruku priblíž viac k pravej ruke.")
                self.naoqi.speak_or_message(sentence_to_say)

        elif "Chyba" in message:
            sentence_to_say = self.warning_sentences.get(
                    "error", "Skús tiež lepšie predpažiť. Dbaj na to aby ruky boli vodorovné s tvojími ramenami.")
            self.naoqi.speak_or_message(sentence_to_say)
