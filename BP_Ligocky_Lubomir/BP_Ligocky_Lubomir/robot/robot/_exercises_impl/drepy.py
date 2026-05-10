# -*- coding: utf-8 -*-

import time
import sys
import os

from robot_exercise_utils import RobotExerciseUtils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sit_exercise

module_path = os.path.join(os.getcwd(), 'sadanie')
if module_path not in sys.path:
    sys.path.append(module_path)

import sitting_position_for_extending_legs as sit_on_chair
import daj_ruky_k_telu_zo_zakladneho_sedu as ruky_k_telu_zo_zakladneho_sedu


class Drepy(RobotExerciseUtils):
    is_ending = False
      
    def __init__(self, naoqi_instance):
        super(Drepy, self).__init__(naoqi_instance)
        self.exercise_name = 'SquatExercise'
        self.score = 0
        self.conn = None
        self.load_exercise_config(self.exercise_name, self.naoqi.lang)
        self.starting_sentence = self.exercise_speach_lang.get("on_start", {}).get("default",
                                                                                   "Začíname cvičiť, drepy. Cvičiť začíname v stoji.")
        self.ending_sentence = self.exercise_speach_lang.get("on_end", {}).get("default",
                                                                               "Výborne, drepy máme za sebou")
        self.warning_sentences = self.exercise_speach_lang.get("on_warning", {})
    
    def run_exercise(self, score, message, conn):
        self.score = score
        self.conn = conn
        print(message)
        if 'squat_start' in message:
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.5)
            self.naoqi.speak_or_message(self.starting_sentence)
            conn.send("ExerciseContinue_tposeE".encode())
          
        elif 'squat_end' in message:
            self.is_ending = True
            """if not self.naoqi.is_physical:
                ending_sentence_part1 = self.exercise_speach_lang.get("on_end", {}).get("end1_part1",
                                                                                  "Ďakujeme za spoluprácu,")
                ending_sentence_part2 = self.exercise_speach_lang.get("on_end", {}).get("end1_part2",
                                                                                        "budeme sa ťešiť aj na budúce.")
            else:
                ending_sentence_part1 = self.exercise_speach_lang.get("on_end", {}).get("end2_part1",
                                                                                        "Ďakujem, že sme spolu cvičili,")
                ending_sentence_part2 = self.exercise_speach_lang.get("on_end", {}).get("end2_part2",
                                                                                        "Nech ťi to vydrží.")
            self.naoqi.speak_or_message(self.ending_sentence)

            time.sleep(0.4)

            self.naoqi.speak_or_message(ending_sentence_part1)
            self.naoqi.speak_or_message(ending_sentence_part2)"""

        elif 'squat_up' in message and self.is_ending is False:

            self.say_score(score, conn)

            new_times2 = []
            for joint_times in sit_exercise.times:
                new_joint_times = [t * 0.5 for t in joint_times]
                new_times2.append(new_joint_times)

            self.naoqi.motionProxy.angleInterpolation(sit_exercise.names, sit_exercise.keys, new_times2, True)

            phase1_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase1.1", "Podrep s nádychom")
            self.naoqi.speak_or_message(phase1_sentence)

            conn.send("ExerciseContinue_squatE".encode())

        elif 'squat_down' == message:
            
            self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.2)

            if (score < 4 and score != 0) or (score == 7):
                phase2_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase2", "Postav sa s výdychom")
            else:
                phase2_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase2.1", "Postav sa")
            self.naoqi.speak_or_message(phase2_sentence)

            conn.send("ExerciseContinue_squatE".encode())
    
    def warning_say(self, message):
        """if self.naoqi.limit - 1 != self.score and "squat_rozpaz_oprava" in message:
            sentence_to_say = self.warning_sentences.get("squat_rozpaz_oprava", "Výborne, teraz po mňe opakuj.")
            self.naoqi.speak_or_message(sentence_to_say)
            if 'Base_pos_back' in message:
                sentence_to_say = self.warning_sentences.get("Base_pos_back", "Už sa postav")
                self.naoqi.speak_or_message(sentence_to_say)
            elif 'Base_pos' in message:
                sentence_to_say = self.warning_sentences.get("Base_pos", "Prosím, spravťe drep")
                self.naoqi.speak_or_message(sentence_to_say)
            elif 'squat_up' in message and self.is_ending is False:
                # self.naoqi.postureProxy.goToPosture(self.zakladna_pozicia_statia, 0.2)

                self.say_score(self.score, self.conn)

                self.naoqi.motionProxy.angleInterpolation(sit_exercise.names, sit_exercise.keys, sit_exercise.times,
                                                          True)
                phase1_sentence = self.exercise_speach_lang.get("on_phase", {}).get("phase1.1", "Podrep s nádychom")
                self.naoqi.speak_or_message(phase1_sentence)

                self.conn.send("ExerciseContinue_squatE".encode())
        elif self.naoqi.limit - 1 == self.score and "squat_rozpaz_oprava" in message:
            sentence_to_say = self.warning_sentences.get("squat_rozpaz_oprava", "")
            self.naoqi.speak_or_message(sentence_to_say)
            if 'Base_pos_back' in message:
                sentence_to_say = self.warning_sentences.get("Base_pos_back", "")
                self.naoqi.speak_or_message(sentence_to_say)
            elif 'Base_pos' in message:
                sentence_to_say = self.warning_sentences.get("Base_pos", "")
                self.naoqi.speak_or_message(sentence_to_say)
        elif "squat_rozpaz" in message:
            sentence_to_say = self.warning_sentences.get("squat_rozpaz", "Prosím, o trošku posuň choďidlá od seba")
            self.naoqi.speak_or_message(sentence_to_say)
        elif "squat_zly_drep" in message:
            sentence_to_say = self.warning_sentences.get("squat_zly_drep", "Ešťe nižšie.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        # Zaklad
        elif 'Base_pos_back' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos_back", "Už sa postav")
            self.naoqi.speak_or_message(sentence_to_say)

        elif 'Base_pos' in message:
            sentence_to_say = self.warning_sentences.get("Base_pos", "Prosím, spravťe drep")
            self.naoqi.speak_or_message(sentence_to_say)


        elif "V_drepe_predpazene_ruky_vysoko_a_odseba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_vysoko_a_odseba",
                                                         "Predpaž ruky viacej k sebe a do nižšej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)

        elif "V_drepe_predpazene_ruky_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_vysoko",
                                                         "Predpaž ruky do nižšej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_predpazene_ruky_nizko_a_odseba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_vysoko",
                                                         "Predpaž ruky viacej k sebe a do vyššiej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_predpazene_ruky_nizko" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_nizko",
                                                         "Predpaž ruky do vyššiej polohy.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        # Ine

        elif "V_drepe_predpazene_ruky_zle" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_zle",
                                                         "Predpažené ruky predpaž na vodorovnú polohu na úroveň tvojích ramien.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_predpazene_ruky_priliz_od_seba" in message:
            sentence_to_say = self.warning_sentences.get("both_hands", {}).get("V_drepe_predpazene_ruky_priliz_od_seba",
                                                         "Predpažené ruky priblíž viacej k sebe.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        # Prava ruka
        
        elif "V_drepe_prava_ruka_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("V_drepe_prava_ruka_vysoko",
                                                                               "Daj pravú ruku nižšie.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_prava_ruka_nizko" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("V_drepe_prava_ruka_nizko",
                                                                               "Daj pravú ruku vyššie.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_prava_ruka_nespravne" in message:
            sentence_to_say = self.warning_sentences.get("right_hand", {}).get("V_drepe_prava_ruka_nespravne",
                                                         "Daj pravú ruku bližšie k lavej.")
            self.naoqi.speak_or_message(sentence_to_say)
            
        
        # lava ruka
        
        elif "V_drepe_lava_ruka_vysoko" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("V_drepe_lava_ruka_vysoko",
                                                         "Daj ľavú ruku nižšie.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_lava_ruka_nizko" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("V_drepe_lava_ruka_nizko",
                                                         "Daj ľavú ruku vyššie.")
            self.naoqi.speak_or_message(sentence_to_say)
        
        elif "V_drepe_lava_ruka_nespravne" in message:
            sentence_to_say = self.warning_sentences.get("left_hand", {}).get("V_drepe_lava_ruka_nespravne",
                                                         "Daj ľavú ruku bližšie k pravej.")
            self.naoqi.speak_or_message(sentence_to_say)

        else:
            if self.naoqi.limit < self.score:
                sentence_to_say = self.warning_sentences.get("left_hand", {}).get("default",
                                                             "Niečo robíž zle.")
                self.naoqi.speak_or_message(sentence_to_say)"""
