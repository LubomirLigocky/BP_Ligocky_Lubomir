from datetime import datetime
import json
import socket
import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# import winsound

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

from exercises_thread.forefooting_on_chair import ForefootingOnChair
from exercises_thread.lift_right_leg import LiftRightLeg
from exercises_thread.lift_left_leg import LiftLeftLeg

from exercises_thread.predpazovanie import Predpazovanie

from realsense_depth import *
import mediapipe as mp
from functools import partial

from camera_thread import CameraThread

import configuration.exercises as exercise_messages_configuration

from exercises_thread.sit_stand_raise_arms import SitStandRaiseArms

from exercises_thread.squat_exercise import SquatExercise
from exercises_thread.arm_circling_exercise import ArmCirclingExercise
from exercises_thread.arm_sit_circling_exercise import ArmCirclingSitExercise


from exercise_app_ui import ExerciseAppUI


WALK_SCORE = 5

class ExerciseApp(QMainWindow):
    init_fer = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        
        self.starting_label = None
        self.active_socket = None

        try:
            with open('config.json', 'r') as config_file:
                self.json_config = json.load(config_file)
        except:
            self.json_config = None
        
        print(self.json_config)

        self.connect_to_robot() # initialize socket connection

        self.current_exercise = None  # Initialize current exercise reference

        self.exercise_messages = exercise_messages_configuration.EXERCISE_MESSAGES
        self.current_exercise_score = 0

        # Set up the camera thread and connect its frame_captured signal to the update_camera slot
        self.camera_thread = CameraThread()
        self.camera_thread.frame_captured.connect(self.update_camera)
        self.camera_thread.update_distance_signal.connect(self.update_distance)
        self.camera_thread.start()
        self.init_fer.connect(self.camera_thread.initialize_fer)

        # GUI
        self.uiWrapper = ExerciseAppUI(self.camera_thread)

        # Prepinanie kamery
        self.uiWrapper.ui.kamera_1.clicked.connect(partial(self.camera_thread.change_camera, 'depth'))
        self.uiWrapper.ui.kamera_2.clicked.connect(partial(self.camera_thread.change_camera, 'distance'))

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
    
    def activate_buttons(self):
         # Connect the button to the start_exercise method
        self.uiWrapper.ui.sadanie_na_stolicku_button.clicked.connect(self.start_sadanie_na_stolicku)

        #Kruzenie
        self.uiWrapper.ui.arm_circling_button.clicked.connect(self.start_arm_circling)
        self.uiWrapper.ui.arm_sit_circling_button.clicked.connect(self.start_sit_arm_circling)

        #Chodenie okolo stolicky
        self.uiWrapper.ui.chair_circling_button.clicked.connect(self.start_chair_circling)
      

        #Zaklad
        self.uiWrapper.ui.tpose_button.clicked.connect(self.start_tpose)
        self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)
        
        # Toto je bez stolicky
        self.uiWrapper.ui.squat_button.clicked.connect(self.start_squat)
        self.uiWrapper.ui.sit_stand_raise_arms_button.clicked.connect(self.start_sit_stand_raise_arms)
        
        # Toto je so stolickou
        self.uiWrapper.ui.forefooting_ruky_pri_tele_button.clicked.connect(self.start_forefooting_ruky_pri_tele)
        self.uiWrapper.ui.forefooting_ruky_nad_hlavu_button.clicked.connect(self.start_forefooting_ruky_nad_hlavu)
        self.uiWrapper.ui.forefooting_predpazovanie_button.clicked.connect(self.start_forefooting_predpazovanie)
        self.uiWrapper.ui.forefooting_rozpazovanie_button.clicked.connect(self.start_forefooting_rozpazovanie)

        # forefooting_in_lying
        self.uiWrapper.ui.forefooting_in_lying_button.clicked.connect(self.start_forefooting_in_lying)
        self.uiWrapper.ui.krizny_forefooting_in_lying_button.clicked.connect(self.start_krizny_forefooting_in_lying)

        self.uiWrapper.ui.predpazovanie_button.clicked.connect(self.start_predpazovanie)

        # End button
        self.uiWrapper.ui.end_button.clicked.connect(self.end_exercise)


        # Gui
        
        self.uiWrapper.ui.note_label.setText("Cvičenie ešte nezačalo")
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
        except:
            self.active_socket = None
            self.starting_label = "Žiadne spojenie"


    def send_config(self):
        self.json_config = self.uiWrapper.show_dialog_config(self.json_config)

        with open('config.json', 'w') as config_file:
            json.dump( self.json_config, config_file, indent=4)
        
        self.connect_to_robot()
        self.activate_FER() # initialize emotion recognition
        self.init_fer.emit(self.detect_em, self.fer_model)


    def update_camera(self, qimage, fer_class):
        # Display the camera frame in the GUI
        self.uiWrapper.ui.video_feed.setPixmap(QPixmap.fromImage(qimage))
        self.uiWrapper.ui.emotion_class.setText(fer_class)
    
    def update_exercise_label(self, note):   # Update the label with the result of the exercise
        self.uiWrapper.ui.note_label.setText(note)

    def update_distance(self, distance):
        self.uiWrapper.ui.distance_label.setText(str(round(distance*0.001, 2)) + " m")

    def end_exercise(self):
        if self.current_exercise:
            self.current_exercise.end_exercise()
            self.current_exercise = None  # Reset the current exercise reference
    
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
        self.current_exercise = SquatExercise(self.exercise_messages["squat"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("squat", increment_score))
        self.current_exercise.start()

    def start_tpose(self, increment_score_bool):
        self.current_exercise = TPoseExercise(self.exercise_messages["tpose"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("tpose", increment_score))
        self.current_exercise.start()

    def start_predpazovanie(self, increment_score_bool):
        self.current_exercise = Predpazovanie(self.exercise_messages["predpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("predpazovanie", increment_score))
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
        self.current_exercise = SadanieNaStolicku(self.exercise_messages["sadanie_na_stolicku"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("sadanie_na_stolicku", increment_score))
        self.current_exercise.start()

    def start_forefooting_arm_raising(self, increment_score_bool):
        self.current_exercise = ForefootingArmRaising(self.exercise_messages["forefooting_arm_raising"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_arm_raising", increment_score))
        self.current_exercise.start()

    def start_forefooting_on_chair(self, increment_score_bool):
        self.current_exercise = ForefootingOnChair(self.exercise_messages["forefooting_on_chair"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_on_chair", increment_score))
        self.current_exercise.start()

    def start_forefooting_ruky_pri_tele(self, increment_score_bool):
        self.current_exercise = ForefootingRukyPriTele(self.exercise_messages["forefooting_ruky_pri_tele"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_ruky_pri_tele", increment_score))
        self.current_exercise.start()

    def start_forefooting_predpazovanie(self, increment_score_bool):
        self.current_exercise = ForefootingPredpazovanie(self.exercise_messages["forefooting_predpazovanie"], self.uiWrapper, self)
        self.camera_thread.score_signal.connect(lambda increment_score=increment_score_bool: self.current_exercise.exercise_update_score("forefooting_predpazovanie", increment_score))
        self.current_exercise.start()

    def start_forefooting_rozpazovanie(self, increment_score_bool):
        self.current_exercise = ForefootingRozpazovanie(self.exercise_messages["forefooting_rozpazovanie"], self.uiWrapper, self)
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
      
        try:
            self.camera_thread.stage_signal.disconnect(self.current_exercise.send_stage_to_robot)
            self.camera_thread.received_robot_signal.disconnect(self.current_exercise.receive_msg_from_robot)
            self.uiWrapper.setStyleSheet("background-color: white;")
           

        except TypeError:
            pass  


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
