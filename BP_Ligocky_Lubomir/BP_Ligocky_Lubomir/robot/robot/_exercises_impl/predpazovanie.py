# -*- coding: utf-8 -*-
import time
import math
import random
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import predpazenie_v_stoji

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import pripazenie_z_predpazenia
import sitting_position_for_extending_legs as sit_on_chair


class Predpazovanie(RobotExerciseUtils):

    def __init__(self, naoqi_instance):
        super(Predpazovanie, self).__init__(naoqi_instance)

        self.exercise_name = 'predpazovanie'
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get("default", "Začíname predpažovať. Buďeme cvičiť v stoji.")
        self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default", "Koniec cvičenia, Pripravíme sa na ďalší cvik.")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})
    
    def run_exercise(self, score, message, pending_messages, phase, conn):
        if message == 'predpazovanie_start,':
            self.remove_items_by_value(pending_messages, score, -1, self.finished_phases, False)

            self.naoqi.speak_or_message(self.starting_sentence)
            conn.send("ExerciseContinue_predpazenie".encode())
            
        if message == 'predpazovanie_en':
            # stand_up_from_chair_times = [[time / self.FAST_MODE_MULTIPLIER for time in times] for times in stand_up_from_chair.times] if self.FAST_MODE else sit_on_chair.times
            # naoqi.motionProxy.angleInterpolationBezier(stand_up_from_chair.names, stand_up_from_chair_times, stand_up_from_chair.keys)

            self.remove_items_by_value(pending_messages, score, -2, self.finished_phases, False)
            self.naoqi.speak_or_message(self.ending_sentence)

        if message == 'predpazovanie':
            if phase == 0 and self.finished_phases["0"] == False:

                self.finished_phases["0"] = True
                self.remove_items_by_value(pending_messages, score, 0, self.finished_phases, False)
                phase1_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase1", "Predpaž.")
                self.naoqi.speak_or_message(phase1_sentence)
                #for index, time_tuple in enumerate(predpazenie_v_stoji.times):
                #    predpazenie_v_stoji[index] = time_tuple[1] + index
                self.naoqi.motionProxy.angleInterpolationBezier(predpazenie_v_stoji.names, predpazenie_v_stoji.times, predpazenie_v_stoji.keys)

                conn.send("ExerciseContinue_predpazenie".encode())
            elif phase == 1 and self.finished_phases["1"] == False:

                self.finished_phases["1"] = True
                self.remove_items_by_value(pending_messages, score, 1, self.finished_phases)
                phase2_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase2", "Pripaž.")
                self.naoqi.speak_or_message(phase2_sentence)
                #self.naoqi.motionProxy.angleInterpolationBezier(predpazenie_v_stoji.names, predpazenie_v_stoji.times,
                #                                                predpazenie_v_stoji.keys)

                self.naoqi.motionProxy.angleInterpolationBezier(pripazenie_z_predpazenia.names, pripazenie_z_predpazenia.times, pripazenie_z_predpazenia.keys)

                conn.send("ExerciseContinue_predpazenie".encode())

            elif phase == 2 and self.finished_phases["2"] == False and self.finished_phases["1"] == True:
                
                self.finished_phases["2"] = True
                self.remove_items_by_value(pending_messages, score, 2, self.finished_phases, False)

                self.say_score(score + 1, conn)

                self.finished_phases = {str(i): False for i in range(6)}
                
                conn.send("ExerciseContinue_predpazenie".encode())

    def warning_say(self, message):
         # - predpazenie
        """if 'Base_pos_back' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos_back", "Vráť ruky dole")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif 'Base_pos' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos", "Prosím predpaž")
            self.naoqi.speak_or_message(sentence_to_say)

        elif 'Predpazovanie_nie_je_zapazovanie' in message:
            sentence_to_say = self.warning_sentences.get("Predpazovanie_nie_je_zapazovanie", "Ruky majú byť predpažené dopredu, a nie dozadu.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_vysoko_a_odseba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_vysoko_a_odseba", "Posuň ruky nižšie na vodorovnu polohu a bližšie k sebe.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_vysoko_a_nespravne" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_vysoko_a_nespravne",
                                                                               "Daj ruky nižšie na vodorovnu úroveň a do správnej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_vysoko",
                                                                               "Skús ruky posunúť nižšie na vodorovnu polohu.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_nizko_a_odseba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_nizko_a_odseba",
                                                                               "Skús ruky posunúť vyššie na vodorovnu polohu a priblížiť ich k sebe.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Predpazene_ruky_nizko_a_nespravne" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_nizko_a_nespravne",
                                                                               "Daj ruky vyššie na vodorovnu úroveň a do správnej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)
               
        elif "Predpazene_ruky_nizko" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_nizko",
                                                                               "Skús ruky posunúť vyššie na vodorovnu polohu.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "Predpazene_ruky_zle" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Predpazene_ruky_zle",
                                                                               "Predpaž ruky do správnej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Upazene_ruky_priliz_od_seba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("Upazene_ruky_priliz_od_seba",
                                                                               "Daj ruky na vodorovnu úroveň a do správnej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)


        # Hlášky pre pravú ruku - predpazenie

        elif "Prava_ruka_vysoko_a_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("Prava_ruka_vysoko_a_od_tela",
                                                                               "Pravú ruku daj trošku nižšie a bližšie k ľavej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("Prava_ruka_vysoko",
                                                                               "Pravú ruku skús dať o trochu nižšie.")
            self.naoqi.speak_or_message(sentence_to_say)
               
        elif "Prava_ruka_nizko_a_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("Prava_ruka_nizko_a_od_tela",
                                                                               "Pravú ruku zdvihni trochu vyššie a bližšie k ľavej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_nizko" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("Prava_ruka_nizko",
                                                                               "Daj pravú ruku trošku vyššie.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Prava_ruka_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("Prava_ruka_od_tela",
                                                                               "Pravú ruku priblíž viac k ľavej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)


        # Hlášky pre ľavú ruku - predpazenie

        elif "Lava_ruka_vysoko_a_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("Lava_ruka_vysoko_a_od_tela",
                                                                               "Ľavú ruku daj trošku nižšie a bližšie k pravej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("Lava_ruka_vysoko",
                                                                               "Ľavú ruku skús dať o trochu nižšie.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_nizko_a_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("Lava_ruka_nizko_a_od_tela",
                                                                              "Ľavú ruku zdvihni trochu vyššie a bližšie k pravej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_nizko" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("Lava_ruka_nizko",
                                                                              "Zdvihni ľavú ruku trošku vyššie.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Lava_ruka_od_tela" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("Lava_ruka_od_tela",
                                                                              "Ľavú ruku priblíž viac k pravej ruke.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "Chyba" in message:
            sentence_to_say = self.warning_sentences.get("default", "Skús lepšie predpažiť.")
            self.naoqi.speak_or_message(sentence_to_say)
        else:
            sentence_to_say = self.warning_sentences.get("default", "Skús lepšie predpažiť.")
            self.naoqi.speak_or_message(sentence_to_say)"""