from datetime import datetime
import json
import socket
import sys
import os
import time
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# import winsound

import pyaudio
import webrtcvad
import wave
import collections
import re
import base64
from openai import OpenAI


from exercises_thread.chair_circling_exercise import ChairCirclingExercise
from exercises_thread.t_pose_exercise import TPoseExercise
from exercises_thread.sadanie_na_stolicku import SadanieNaStolicku

from exercises_thread.forefooting_arm_raising import ForefootingArmRaising
from exercises_thread.forefooting_in_lying import ForefootingInLying
from exercises_thread.krizny_forefooting_in_lying import KriznyForefootingInLying

from exercises_thread.forefooting_ruky_nad_hlavu import ForefootingRukyNadHlavu
from exercises_thread.forefooting_ruky_pri_tele import ForefootingRukyPriTele
from exercises_thread.forefooting_predpazovanie import ForefootingPredpazovanie
from exercises_thread.forefooting_rozpazovanie import ForefootingRozpazovanie
from exercises_thread.knee_lifting_predpazovanie import KneeLiftingPredpazovanie
from exercises_thread.knee_lifting_rozpazovanie import KneeLiftingRozpazovanie


from exercises_thread.forefooting_on_chair import ForefootingOnChair
from exercises_thread.lift_right_leg import LiftRightLeg
from exercises_thread.lift_left_leg import LiftLeftLeg

from exercises_thread.predpazovanie import Predpazovanie

from functools import partial

from camera_thread import CameraThread

import configuration.exercises as exercise_messages_configuration

from exercises_thread.sit_stand_raise_arms import SitStandRaiseArms

from exercises_thread.squat_exercise import SquatExercise
from exercises_thread.arm_circling_exercise import ArmCirclingExercise
from exercises_thread.arm_sit_circling_exercise import ArmCirclingSitExercise


from exercise_app_ui import ExerciseAppUI


WALK_SCORE = 5

class VoiceAssistantThread(QThread):
    force_end_signal = Signal()

    def __init__(self, nao_ip, parent=None):
        super().__init__(parent)
        self.nao_ip = nao_ip
        self.nao_port = 5005
        self.running = True
        self.is_robot_speaking = False

        self.current_exercise_name = "žiadne"
        self.current_score = 0
        self.current_stage = "neznáma"
        
        # OPENAI configuration
        self.OPENAI_API_KEY = ""   #insert your openai API key here 
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.conversation_history = []
        
        #removing emojis from message
        self.emoji_pattern = re.compile(
            "[" "\U0001F600-\U0001F64F" "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF" "\U0001F1E0-\U0001F1FF"
            "\U00002700-\U000027BF" "\U0001F900-\U0001F9FF"
            "\U0001FA70-\U0001FAFF" "\U00002600-\U000026FF" "]+",
            flags=re.UNICODE
        )

    def remove_emoji(self, text):
        return self.emoji_pattern.sub("", text)

    def initialize_robot_context(self):
        print("--- Kalibrujem audio model.. ---")
        system_prompt = """
        CIEĽ: Si NAO- empatický a profesionálny asistent cvičenia pre seniorov. Tvojou úlohou je v reálnom čase monitorovať seniora cez audio vstup a dynamicky prispôsobovať interakciu.

        Nachádzaš sa v menšej dobre osvetlenej miestnosti spolu s cvičiacim subjektom, ktorému ukazuješ ako správne exekuovať dané cviky a on po tebe opakuje. 

        ANALÝZA (HLAVNÁ ÚLOHA):
        Využi schopnosť audio modelu na analýzu nielen obsahu, ale aj akustických parametrov:
        1. Akustické parametre: Sleduj dych (lapanie po dychu, dýchavičnosť), stabilitu hlasu (tras, neistota), paralingvistické javy (vzdychanie, stonanie, smiech).
        2. Sémantický obsah: Deteguj sťažnosti na bolesť, únavu alebo naopak vyjadrenie radosti a motivácie.
        3. Sentiment: Vyhodnoť emocionálne rozpoloženie (frustrácia, spokojnosť, strach).

        KATEGORIZÁCIA STAVU:
        - "v poriadku": Plynulá reč, pravidelný dych, pozitívny alebo neutrálny tón.
        - "trochu unavený": Mierne zrýchlený dych, dlhšie pauzy medzi slovami, subjektívne vyjadrenie námahy.
        - "unavený": Ťažké lapanie po dychu, výrazný tras v hlase, sťažnosti na bolesť, neschopnosť dohovoriť vetu.

        PRAVIDLÁ INTERAKCIE (ODPOVEĎ PRE NAO):
        - Rešpektuj inkluzívny dizajn: Hovor slovensky, v krátkych, jasných a zrozumiteľných vetách (max. 15 slov).
        - Buď motivačný, ale prioritizuj bezpečnosť.
        - Ak je senior "trochu unaveny", prispôsob sa situácii podla sentimentu a nálady: ak je negatívny navrhni mu krátku prestávku, ak je pozitívny jemne ho povzbuď, aby sa prekonal a docvičil
        - Ak je "unaveny", oznám mu, že cvičenie pre jeho bezpečnosť je dobré prerušiť a spytaj sa či chce cvičenie úplne ukončiť.
        - Nepoužívaj hviezdičky (*) ani emotikony.

        VÝSTUPNÝ FORMÁT (striktný JSON):
        {
        "stav_seniora": "v poriadku" | "trochu unaveny" | "unaveny" | "ukoncenie"(iba ak ti v nadväznosti na únavu vyslovene povie že chce ukončiť cvičenie),
        "analyza_hlasu": "Stručný odborný opis akustických a sémantických javov (napr. 'Zistená mierna dýchavičnosť a pozitívny sentiment').",
        "odpoved_pre_nao": "Text, ktorý robot NAO nahlas povie seniorovi."
        }
        """
        self.conversation_history.append({"role": "system", "content": system_prompt})
        print("--- Kalibrácia hotová ---")

    def record_audio(self):
        vad = webrtcvad.Vad(3) 
        RATE, FRAME_DURATION = 16000, 30
        FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
        AUDIO_FILENAME = "speech.wav"
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=FRAME_SIZE)
        ring_buffer = collections.deque(maxlen=40)
        recording = []
        triggered = False

        print("+++ Mikrofón pripravený, počúvam... +++")

        while self.running:
            # Interruption check, stops recording
            if self.is_robot_speaking:
                print("[DEBUG] robot hovorí, prerušujem nahrávanie mikrofónom")
                stream.stop_stream()
                stream.close()
                audio.terminate()
                return None 

            try:
                frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
                speech = vad.is_speech(frame, RATE)

                if not triggered:
                    ring_buffer.append((frame, speech))
                    num_speech = sum(1 for f, s in ring_buffer if s)
                    if num_speech > 20:
                        triggered = True
                        recording.extend(f for f, s in ring_buffer)
                        ring_buffer.clear()
                else:
                    recording.append(frame)
                    ring_buffer.append((frame, speech))
                    num_silence = sum(1 for f, s in ring_buffer if not s)
                    
                    if num_silence > 30: 
                        wf = wave.open(AUDIO_FILENAME, "wb")
                        wf.setnchannels(1)
                        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(recording))
                        wf.close()
                        
                        stream.stop_stream()
                        stream.close()
                        audio.terminate()
                        return AUDIO_FILENAME

            except Exception as e:
                print(f"Chyba pri nahrávaní: {e}")
                break

        try:
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except:
            pass
        return None

    def chat_with_audio_model(self, audio_path):
        try:
            with open(audio_path, "rb") as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
            
            #text description of current status
            context_text = (f"Aktuálne cvičenie: {self.current_exercise_name}. "
                            f"Počet opakovaní (skóre): {self.current_score}. "
                            f"Fáza cvičenia: {self.current_stage}.")

            user_message = {
                "role": "user",
                "content": [
                    {"type": "text", "text": context_text},
                    {"type": "input_audio", "input_audio": {"data": encoded_audio, "format": "wav"}}
                ]
            }
            
            response = self.client.chat.completions.create(
                model="gpt-4o-audio-preview", 
                modalities=["text"], 
                messages=self.conversation_history + [user_message], 
                temperature=0.2
            )
            raw_response = response.choices[0].message.content
            cleaned_json = raw_response.replace("```json", "").replace("```", "").strip()
            ai_data = json.loads(cleaned_json)
            
            self.conversation_history.append(user_message)
            self.conversation_history.append({"role": "assistant", "content": raw_response})
            if len(self.conversation_history) > 15:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-10:]
            return ai_data
        except Exception as e:
            return None
        
    def update_exercise_context(self, name, score, stage):
        self.current_exercise_name = name
        self.current_score = score
        self.current_stage = stage

    def send_to_nao(self, text):
        try:
            self.is_robot_speaking = True
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(20) 
            sock.connect((self.nao_ip, self.nao_port))
            
            # sending bytes
            sock.sendall(text.encode('utf-8'))
            
            # receiving bytes
            data = sock.recv(1024)
            print(f"Prijate od robota: {data}")

            if b"FINISHED_SPEAKING" in data:
                print("+++ Robot skončil, zapínam nahrávanie mikrofónom. +++")
                
            sock.close()
        except Exception as e:
            print(f"[Voice Chyba] {e}")
        finally:
            self.is_robot_speaking = False

    def run(self):
        self.initialize_robot_context()
        while self.running:
            # checking if robot is speaking
            if self.is_robot_speaking:
                print("--spím...(0.2s)")
                time.sleep(0.2)
                continue

            audio_file = self.record_audio()

            # audio processing
            if audio_file:
                try:
                    ai_data = self.chat_with_audio_model(audio_file)
                    if ai_data:
                        stav = ai_data.get("stav_seniora", "").lower()
                        analyza = ai_data.get("analyza_hlasu", "")
                        text_pre_nao = ai_data.get("odpoved_pre_nao", "")
                        
                        print(f"\n[MONITORING HLASU] Stav: {stav.upper()} | Analýza: {analyza}")
                        text_pre_nao = self.remove_emoji(text_pre_nao).replace("*", "")
                        
                        self.send_to_nao(text_pre_nao)

                        # terminate exercise if requested
                        if stav == "ukoncenie":
                            print("[DEBUG] Senior chce skončiť. Vysielam signál na ukončenie cviku.")
                            self.force_end_signal.emit()
                            self.running = False 
                            break 
    
                except Exception as e:
                    print(f"Chyba pri spracovaní AI: {e}")
    

    def stop(self):
        self.running = False
        self.wait()


class ExerciseApp(QMainWindow):
    init_fer = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        
        self.starting_label = None
        self.active_socket = None
        self.lang = "sk"
        self.__load_base_config(self.lang)
        try:
            with open('config.json', 'r') as config_file:
                self.json_config = json.load(config_file)
        except:
            self.json_config = None
        
        print(self.json_config)
        self.current_exercise = None  # Initialize current exercise reference

        self.exercise_messages = exercise_messages_configuration.EXERCISE_MESSAGES

        # Set up the camera thread and connect its frame_captured signal to the update_camera slot
        self.camera_thread = CameraThread()
        #self.camera_thread.frame_captured.connect(self.update_camera)
        self.camera_thread.video_stream.connect(self.update_camera)
        self.camera_thread.update_distance_signal.connect(self.update_distance)
        self.camera_thread.start()
        self.init_fer.connect(self.camera_thread.initialize_fer)

        self.connect_to_robot()  # initialize socket connection
        # GUI
        self.uiWrapper = ExerciseAppUI(self.camera_thread, self.active_socket,
                                       base_speach_lang=self.base_speach_lang, json_config=self.json_config)

        # Prepinanie kamery
        self.uiWrapper.ui.kamera_1.clicked.connect(partial(self.camera_thread.change_camera, 'depth'))
        self.uiWrapper.ui.kamera_2.clicked.connect(partial(self.camera_thread.change_camera, 'side'))

        self.uiWrapper.ui.config_button.clicked.connect(self.send_config)
        self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)

        if self.active_socket != None:
            self.activate_buttons()
        else:
            self.uiWrapper.ui.note_label.setText(self.starting_label)
        
        self.activate_FER() # initialize emotion recognition
        self.init_fer.emit(self.detect_em, self.fer_model)
           
       
        # Set up the timer
        self.elapsed_time = 0
        self.remaining_time = 10

    def sync_voice_context(self, name):
        if hasattr(self, 'voice_thread') and self.current_exercise:
            name = self.current_exercise.__class__.__name__
            score = self.uiWrapper.ui.score_label.text()
            stage = getattr(self.current_exercise, 'current_stage', "aktívne")
            
            self.voice_thread.update_exercise_context(name, score, stage)

    def __load_base_config(self, lang):
        path_to_base_file = "lang/" + str(lang) + ".json"

        with open(path_to_base_file, "r", encoding="utf-8") as file:
            self.base_speach_lang = json.loads(file.read())

    def activate_buttons(self):
         # Connect the button to the start_exercise method
        self.uiWrapper.ui.sadanie_na_stolicku_button.clicked.connect(self.start_sadanie_na_stolicku)

        #Kruzenie
        self.uiWrapper.ui.arm_circling_button.clicked.connect(self.start_arm_circling)
        self.uiWrapper.ui.arm_sit_circling_button.clicked.connect(self.start_sit_arm_circling)

        #Chodenie okolo stolicky
        #self.uiWrapper.ui.chair_circling_button.clicked.connect(self.start_chair_circling)

        #Zaklad
        self.uiWrapper.ui.tpose_button.clicked.connect(self.start_tpose)
        #self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)
        
        # Toto je bez stolicky
        self.uiWrapper.ui.squat_button.clicked.connect(self.start_squat)
        #self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)
        self.uiWrapper.ui.sit_stand_raise_arms_button.clicked.connect(self.start_sit_stand_raise_arms)
        
        # Toto je so stolickou
        self.uiWrapper.ui.forefooting_ruky_pri_tele_button.clicked.connect(self.start_forefooting_ruky_pri_tele)
        self.uiWrapper.ui.forefooting_ruky_nad_hlavu_button.clicked.connect(self.start_forefooting_ruky_nad_hlavu)
        self.uiWrapper.ui.forefooting_predpazovanie_button.clicked.connect(self.start_forefooting_predpazovanie)
        self.uiWrapper.ui.forefooting_rozpazovanie_button.clicked.connect(self.start_forefooting_rozpazovanie)

        self.uiWrapper.ui.knee_lifting_predpazovanie_button.clicked.connect(self.start_knee_lifting_predpazovanie)
        self.uiWrapper.ui.knee_lifting_rozpazovanie_button.clicked.connect(self.start_knee_lifting_rozpazovanie)

        # forefooting_in_lying
        self.uiWrapper.ui.forefooting_in_lying_button.clicked.connect(self.start_forefooting_in_lying)
        self.uiWrapper.ui.krizny_forefooting_in_lying_button.clicked.connect(self.start_krizny_forefooting_in_lying)

        self.uiWrapper.ui.predpazovanie_button.clicked.connect(self.start_predpazovanie)

        # End button
        self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)

        # Gui
        not_started_exercise = self.base_speach_lang.get("exercise_phases", {}).get("not_launched", "Cvičenie ešte nezačalo")
        self.uiWrapper.ui.note_label.setText(not_started_exercise)
        self.uiWrapper.ui.distance_label.setText(" - ")
        self.uiWrapper.ui.score_label.setText("0")

    def activate_FER(self):
         # Facial emotion recognition setup
        if self.json_config != None:
            self.detect_em = self.json_config['enable_emotions']
            self.fer_model = exercise_messages_configuration.FER_MODEL
                    
        else:
            self.detect_em = False
            self.fer_model = ''
    
    def connect_to_robot(self):
        try:
            if self.active_socket == None:

                ip_adress = (self.json_config["server_ip"], int(self.json_config["server_port"]))

                self.active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.active_socket.connect(ip_adress)
                self.active_socket.setblocking(False) # Necessary, dont change or program will freeze
            config_message = "config;" + json.dumps(self.json_config)

            print("Sended config...", config_message)
            self.active_socket.sendall(config_message.encode())

            self.voice_thread = VoiceAssistantThread(nao_ip=self.json_config["server_ip"])
            self.voice_thread.force_end_signal.connect(QApplication.instance().quit)
            self.voice_thread.start()
        except:
            self.active_socket = None
            self.starting_label = self.base_speach_lang.get("connection", {}).get("no_connection",
                                                                                        "Žiadne spojenie")

    def send_config(self):
        self.json_config = self.uiWrapper.show_dialog_config(self.json_config)
        self.json_config["lang"] = "sk"

        with open('config.json', 'w') as config_file:
            json.dump( self.json_config, config_file, indent=4)
        
        self.connect_to_robot()
        self.activate_FER() # initialize emotion recognition
        self.init_fer.emit(self.detect_em, self.fer_model)


    def update_camera(self, qimage, fer_class):
        # Display the camera frame in the GUI
        self.uiWrapper.ui.video_feed.setPixmap(QPixmap.fromImage(qimage))
        #self.uiWrapper.ui.emotion_class.setText(fer_class)
    
    def update_exercise_label(self, note):   # Update the label with the result of the exercise
        self.uiWrapper.ui.note_label.setText(note)

    def update_distance(self, distance):
        self.uiWrapper.ui.distance_label.setText(str(round(distance*0.001, 2)) + " m")

    def start_chair_circling(self, increment_score_bool):
        self.current_exercise = ChairCirclingExercise(self.exercise_messages["chair_circling"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("chair_circling", increment_score))
        self.current_exercise.start()
    
    def start_arm_circling(self, increment_score_bool):
        self.current_exercise = ArmCirclingExercise(self.exercise_messages["arm_circling"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("arm_circling", increment_score))
        self.current_exercise.start()
    
    def start_sit_arm_circling(self, increment_score_bool):
        self.current_exercise = ArmCirclingSitExercise(self.exercise_messages["arm_sit_circling"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("arm_sit_circling", increment_score))
        self.current_exercise.start()

    def start_squat(self, increment_score_bool):
        increment_score_bool = 1 if increment_score_bool else 0
        self.current_exercise = SquatExercise(self.exercise_messages["squat"], self.uiWrapper, self)
        
        # Spustí obe funkcie za sebou v rámci jedného zoznamu
        self.camera_thread.score_signal.connect(
            lambda inc=increment_score_bool: [
                self.current_exercise.exercise_update_score("squat", inc),
                self.sync_voice_context("squat")
            ]
        )
        self.current_exercise.start()

    def start_tpose(self, increment_score_bool):
        increment_score_bool = 1 if increment_score_bool else 0
        self.current_exercise = TPoseExercise(self.exercise_messages["tpose"], self.uiWrapper, self)
        
        # Spustí obe funkcie za sebou v rámci jedného zoznamu
        self.camera_thread.score_signal.connect(
            lambda inc=increment_score_bool: [
                self.current_exercise.exercise_update_score("tpose", inc),
                self.sync_voice_context("tpose")
            ]
        )
        self.current_exercise.start()

    def start_predpazovanie(self, increment_score_bool):
        increment_score_bool = 1 if increment_score_bool else 0
        self.current_exercise = Predpazovanie(self.exercise_messages["predpazovanie"], self.uiWrapper, self)
        
        # Spustí obe funkcie za sebou v rámci jedného zoznamu
        self.camera_thread.score_signal.connect(
            lambda inc=increment_score_bool: [
                self.current_exercise.exercise_update_score("predpazovanie", inc),
                self.sync_voice_context("predpazovanie")
            ]
        )
        self.current_exercise.start()

    def start_lift_right_leg(self, increment_score_bool):
        self.current_exercise = LiftRightLeg(self.exercise_messages["lift_right_leg"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("lift_right_leg", increment_score))
        self.current_exercise.start()
        
    def start_lift_left_leg(self, increment_score_bool):
        self.current_exercise = LiftLeftLeg(self.exercise_messages["lift_left_leg"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("lift_left_leg", increment_score))
        self.current_exercise.start()

    def start_sadanie_na_stolicku(self, increment_score_bool):
        self.end_exercise()
        self.current_exercise = SadanieNaStolicku(self.exercise_messages["sadanie_na_stolicku"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("sadanie_na_stolicku", increment_score))
        self.current_exercise.start()

    def start_forefooting_arm_raising(self, increment_score_bool):
        self.end_exercise()
        self.current_exercise = ForefootingArmRaising(self.exercise_messages["forefooting_arm_raising"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_arm_raising", increment_score))
        self.current_exercise.start()

    def start_forefooting_on_chair(self, increment_score_bool):
        self.end_exercise()
        self.current_exercise = ForefootingOnChair(self.exercise_messages["forefooting_on_chair"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_on_chair", increment_score))
        self.current_exercise.start()

    def start_forefooting_ruky_pri_tele(self, increment_score_bool):
        self.end_exercise()
        self.current_exercise = ForefootingRukyPriTele(self.exercise_messages["forefooting_ruky_pri_tele"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_ruky_pri_tele", increment_score))
        self.current_exercise.start()

    def start_forefooting_predpazovanie(self, increment_score_bool):
        self.current_exercise = ForefootingPredpazovanie(self.exercise_messages["forefooting_predpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_predpazovanie", increment_score))
        self.current_exercise.start()

    def start_forefooting_rozpazovanie(self, increment_score_bool):
        self.current_exercise = ForefootingRozpazovanie(self.exercise_messages["forefooting_rozpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_predpazovanie", increment_score))
        self.current_exercise.start()

    def start_knee_lifting_predpazovanie(self, increment_score_bool):
        self.current_exercise = KneeLiftingPredpazovanie(self.exercise_messages["knee_lifting_predpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_rozpazovanie", increment_score))
        self.current_exercise.start()

    def start_knee_lifting_rozpazovanie(self, increment_score_bool):
        self.current_exercise = KneeLiftingRozpazovanie(self.exercise_messages["knee_lifting_rozpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_rozpazovanie", increment_score))
        self.current_exercise.start()

    def start_forefooting_ruky_nad_hlavu(self, increment_score_bool):
        self.current_exercise = ForefootingRukyNadHlavu(self.exercise_messages["forefooting_ruky_nad_hlavu"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_ruky_nad_hlavu", increment_score))
        self.current_exercise.start()

    def start_sit_stand_raise_arms(self, increment_score_bool):
        self.current_exercise = SitStandRaiseArms(self.exercise_messages["sit_stand_raise_arms"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("sit_stand_raise_arms", increment_score))
        self.current_exercise.start()

    def start_forefooting_in_lying(self, increment_score_bool):
        self.current_exercise = ForefootingInLying(self.exercise_messages["forefooting_in_lying"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_in_lying", increment_score))
        self.current_exercise.start()

    def start_krizny_forefooting_in_lying(self, increment_score_bool):
        self.current_exercise = KriznyForefootingInLying(self.exercise_messages["krizny_forefooting_in_lying"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("krizny_forefooting_in_lying", increment_score))
        self.current_exercise.start()

    def update_score_lift_left_leg(self, increment_score_bool):
        self.camera_thread.score_signal.connect(self.exercise_update_score("lift_left_leg", increment_score_bool))

    def lift_left_leg_exercise(self):
        self.camera_thread.frame_captured.connect(self.camera_thread.check_lift_left_leg_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_exercise_label)
        self.camera_thread.score_signal.connect(self.update_score_lift_left_leg)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot)

    def update_score_lift_right_leg(self, increment_score_bool):
        self.camera_thread.score_signal.connect(self.exercise_update_score("lift_right_leg", increment_score_bool))

    def lift_right_leg_exercise(self):
        self.camera_thread.frame_captured.connect(self.camera_thread.check_lift_right_leg_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_exercise_label)
        self.camera_thread.score_signal.connect(self.update_score_lift_right_leg)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot)

    def end_exercise(self):
        if self.camera_thread and self.current_exercise:
            self.current_exercise.end_exercise()
            self.current_exercise.elapsed_time = 0
            try:
                self.camera_thread.stage_signal.disconnect(self.current_exercise.send_stage_to_robot)
                self.camera_thread.received_robot_signal.disconnect(self.current_exercise.receive_msg_from_robot)
            except TypeError:
                pass
        self.current_exercise = None  # Reset the current exercise reference
        self.uiWrapper.setStyleSheet("background-color: white;")
        self.uiWrapper.update_score(0)

    def save_score(self, exercise_name):   # save the time of saving, score and elapsed time to the .txt file
        with open("score.txt", "a") as file:
            file.write(str(datetime.now()) + " " + exercise_name + " " + self.uiWrapper.ui.score_label.text() + " " + str(self.elapsed_time) + "\n")

    def timerEvent(self, event):
        if self.current_exercise is not None:
            self.current_exercise.elapsed_time += 1
            self.uiWrapper.ui.timer_label.setText(str(self.current_exercise.elapsed_time) + " s")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExerciseApp()
    # Run the application event loop
    sys.exit(app.exec())
