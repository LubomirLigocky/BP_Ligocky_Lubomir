# -*- coding: utf-8 -*-

import sys
import os

from robot_exercise_utils import RobotExerciseUtils

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

module_path = os.path.join(os.getcwd(), 'lah')
if module_path not in sys.path:
    sys.path.append(module_path)

import prava_noha_vyrovnaj_po_zakl_lahu
import vyrovna_ruky_v_lahu_vedla_tela

import daj_ruky_hore_v_lahu
import daj_ruky_k_telu_v_lahu


module_path = os.path.join(module_path, 'only_legs_up')
if module_path not in sys.path:
    sys.path.append(module_path)

import iba_lava_noha_hore
import iba_prava_noha_hore
import iba_prava_noha_naspat
import iba_lava_noha_naspat


class ForefootingInLying(RobotExerciseUtils):

    def __init__(self, naoqi_instance):
        super(ForefootingInLying, self).__init__(naoqi_instance)
        self.is_lying = True

        self.exercise_name = "forefooting_in_lying"
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get(
            "default", "Ľahňi si na chrbát a vystri ruky nad hlavu.")
        self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default",
                                                                               "Koniec cvičenia, Pripravíme sa na ďalší cvik.")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})

    def go_down(self):
        self.naoqi.postureProxy.goToPosture("LyingBack", 1.0)
        self.naoqi.motionProxy.angleInterpolationBezier(vyrovna_ruky_v_lahu_vedla_tela.names, vyrovna_ruky_v_lahu_vedla_tela.times, vyrovna_ruky_v_lahu_vedla_tela.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(prava_noha_vyrovnaj_po_zakl_lahu.names, prava_noha_vyrovnaj_po_zakl_lahu.times, prava_noha_vyrovnaj_po_zakl_lahu.keys)
        self.naoqi.motionProxy.angleInterpolationBezier(daj_ruky_hore_v_lahu.names, daj_ruky_hore_v_lahu.times, daj_ruky_hore_v_lahu.keys)
    
    def go_up(self):
        self.naoqi.postureProxy.goToPosture("Stand", 1.0)
        self.naoqi.speak_or_message(self.ending_sentence)

    def say_lying_emotion(self, message):
        if "start" in message:
            self.say_emotion_start(message, self.starting_sentence)
            self.go_down()
        elif "end" in message:
            self.say_emotion_end(message)
            self.go_up()

    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'forefooting_in_lying_start,':
            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases)

            self.naoqi.speak_or_message(self.starting_sentence)
            self.go_down()
            conn.send("ExerciseContinue_lying".encode())

        if message == 'forefooting_in_lying_en':
            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)

            self.naoqi.motionProxy.angleInterpolationBezier(daj_ruky_k_telu_v_lahu.names, daj_ruky_k_telu_v_lahu.times, daj_ruky_k_telu_v_lahu.keys)
            self.go_up()
            conn.send("ExerciseContinue_lying".encode())

        if message == 'forefooting_in_lying':
            if phase == 0 and self.finished_phases["0"] == False: # We put robot to sit first, so we do it in start

                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(iba_prava_noha_hore.names, iba_prava_noha_hore.times, iba_prava_noha_hore.keys)
                
                conn.send(("ExerciseContinue_lying" + str(phase)).encode())

            elif phase == 1 and self.finished_phases["1"] == False and self.finished_phases["0"] == True:
                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(iba_prava_noha_naspat.names, iba_prava_noha_naspat.times, iba_prava_noha_naspat.keys)
                conn.send(("ExerciseContinue_lying" + str(phase)).encode())

            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:
                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(iba_lava_noha_hore.names, iba_lava_noha_hore.times, iba_lava_noha_hore.keys)
                conn.send(("ExerciseContinue_lying" + str(phase)).encode())

            elif phase == 3 and self.finished_phases["3"] == False and self.finished_phases["2"] == True:
                self.finished_phases["3"] = True
                self.remove_items_by_value(pending_messages, score, 3, self.finished_phases)

                self.naoqi.motionProxy.angleInterpolationBezier(iba_lava_noha_naspat.names, iba_lava_noha_naspat.times, iba_lava_noha_naspat.keys)
                
                conn.send(("ExerciseContinue_lying" + str(phase)).encode())

            elif phase == 4 and self.finished_phases["4"] == False and self.finished_phases["3"] == True:

                self.finished_phases["4"] = True
                
                self.say_score(score + 1, conn)
                self.remove_items_by_value(pending_messages, score, 4, self.finished_phases, False)

                self.finished_phases = {str(i): False for i in range(6)}
                
                conn.send(("ExerciseContinue_lying" + str(phase)).encode())
                    
    def warning_say(self, message):
        if "reverse_pose" in message:
            sentence_to_say = self.warning_sentences.get("reverse_pose", "Zdvihli ste opačnú nohu.")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        elif "raised_both_hands" in message:
            sentence_to_say = self.warning_sentences.get("raised_both_hands", "Prosím vráťte obe ruky na zem.")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        elif "raised_left_hand" in message:
            sentence_to_say = self.warning_sentences.get("raised_left_hand", "Prosím vráťte ľavú ruku na zem.")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        elif "raised_right_hand" in message:
            sentence_to_say = self.warning_sentences.get("raised_right_hand", "Prosím vráťte pravú ruku na zem.")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        elif "wrong_pose" in message:
            sentence_to_say = self.warning_sentences.get("wrong_pose", "Cvičenie vykonávate zle.")
            self.naoqi.speak_or_message(sentence_to_say)
            return
        
        elif "wrong_lift" in message:
            sentence_to_say = self.warning_sentences.get("wrong_lift", "Zdvíhate nespravnú ruku a nohu.")
            self.naoqi.speak_or_message(sentence_to_say)
            return
        
        elif "base_pose_1" in message:
            sentence_to_say = self.warning_sentences.get("base_pose_1", "Prosím zdvihnite pravú nohu")
            self.naoqi.speak_or_message(sentence_to_say)
            return

        elif "base_pose_2" in message:
            sentence_to_say = self.warning_sentences.get("base_pose_2", "Prosím zdvihnite ľavú nohu")
            self.naoqi.speak_or_message(sentence_to_say)
            return
        
        # *************************************
        
        elif "Iba_prava_noha_nizko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_prava_noha_nizko", "Pravú nohu viacej vystriťe dohora.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Iba_prava_noha_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_prava_noha_daleko", "Pravú nohu máte príliš naklonenú k vašej hlave, otočťe ju dohora.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Iba_lava_ruka_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_lava_ruka_daleko", "Ľavú ruku máte príliš naklonenú k vašej hlave, otočťe ju dohora.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Iba_lava_noha_nizko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_lava_noha_nizko",
                                                         "Ľavú nohu viacej vystriťe dohora.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Iba_lava_noha_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_lava_noha_daleko",
                                                         "Ľavú nohu máte príliš naklonenú k vašej hlave, otočťe ju dohora.")
            self.naoqi.speak_or_message(sentence_to_say)


        
        elif "Iba_prava_ruka_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Iba_prava_ruka_daleko",
                                                         "Pravú ruku máte príliš naklonenú k vašej hlave, otočťe ju dohora.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Ruka_a_noha_nizko" in message:
            sentence_to_say = self.warning_sentences.get("Ruka_a_noha_nizko",
                                                         "Vystretú nohu otočťe viacej hore.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Ruka_a_noha_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Ruka_a_noha_daleko",
                                                         "Vystretá noha je príliš posunutá k vašej hlave, dajťe ju viacej dohora.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        # *************************************

        elif "Prava_noha_daleko_a_lava_ruka_nizko" in message:
            sentence_to_say = self.warning_sentences.get("Prava_noha_daleko_a_lava_ruka_nizko",
                                                         "Vystretú nohu nemáťe v kolmej pozícií.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Prava_noha_nizko_a_lava_ruka_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Prava_noha_nizko_a_lava_ruka_daleko",
                                                         "Vystretú nohu nemáťe v kolmej pozícií.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_nizko_a_lava_noha_daleko" in message:
            sentence_to_say = self.warning_sentences.get("Prava_ruka_nizko_a_lava_noha_daleko",
                                                         "Vystretú nohu  nemáťe v kolmej pozícií.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Prava_ruka_daleko_a_lava_noha_nizko" in message:
            sentence_to_say = self.warning_sentences.get("Prava_ruka_daleko_a_lava_noha_nizko",
                                                         "Vystretú nohu nemáťe v kolmej pozícií.")
            self.naoqi.speak_or_message(sentence_to_say)
        