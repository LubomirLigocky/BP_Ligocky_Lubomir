import configuration.exercises as exercise_messages_configuration
# import winsound
# from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from datetime import datetime
from PySide6.QtCore import QObject, Signal
import time

class Exercise(QObject):

    exercise_ended = Signal()
    exercise_state_changed_signal = Signal(str)

    def __init__(self, messages, widget, app_instance):
        super().__init__()  # Initialize the QObject base class

        self.app = app_instance  # Now app is the instance of ExerciseApp
        self.uii = app_instance.uiWrapper.ui  # Assuming uiWrapper holds the UI

        self.timer_id = None  # Initialize the timer_id here
        self.widget = widget
        self.ui = widget.ui
        self.camera_thread = widget.camera_thread
        self.messages = messages

        self.elapsed_time = 0

        self.score_limit = int(self.app.json_config["exercise_duration"])

    def start(self):
    
        print(self.start_msg)
        self.app.active_socket.sendall(self.start_msg.encode())
            
        self.widget.setStyleSheet("background-color: white;")
        self.ui.note_label.setText(self.messages['note'])
        
        getattr(self.ui, self.messages['name'] + "_button").setEnabled(False)
        
        # Start the specific exercise function
        getattr(self, self.messages['checker'])()

    def end(self):
        # common behaviors for all exercises when ending
        pass

    def update_label(self, note):
        # Update the label with the result of the exercise
        self.ui.note_label.setText(note)

    def exercise_update_score(self, exercise_name, increment_score_bool):
        exercise = self.messages
        # self.camera_thread.score_signal.connect(self.update_score_tpose)
        current_score = int(self.ui.score_label.text())

        if current_score == self.score_limit:

            setattr(self.camera_thread, f"{exercise_name}_exercise_finished", True)
            self.widget.setStyleSheet("background-color: limegreen;")
            self.save_score(exercise_name)
            print(f"Exercise {exercise_name} ended with score: {current_score}")
            print("Time elapsed: " + str(self.elapsed_time) + " s")

            if self.timer_id is not None:
                print("KILLING TIMER")
                print(self.timer_id)
                self.app.killTimer(self.timer_id)
                self.timer_id = None
           
            # Reset the timer label
            self.elapsed_time = 0
            self.ui.timer_label.setText(str(self.elapsed_time) + " s")
            self.ui.score_label.setText("0")
            self.ui.note_label.setText(exercise["note"].replace("CVIČENIE", "KONIEC CVIKU"))
            
            self.camera_thread.frame_captured.disconnect(getattr(self.camera_thread, f"check_current_exercise"))
            self.app.active_socket.sendall(exercise["end_msg"].encode())

            if self.camera_thread.can_detect_em:
               self.camera_thread.check_response_end = True

            else:
                self.end_exercise()
            

        if increment_score_bool:
            print(self.score_limit)
            self.ui.score_label.setText(str(current_score + 1))

    def end_exercise(self):
        try:
            self.camera_thread.exercise_label_signal.disconnect(self.update_exercise_label)
            # self.camera_thread.stage_signal.disconnect(self.send_stage_to_robot)
            # self.camera_thread.received_message_signal.disconnect(self.show_message_from_robot)
        except RuntimeError as e:
            print(f"Error while disconnecting signals: {e}")

    # tu sa komunikuje z robotom
    def receive_msg_from_robot(self):
        try:
            response = self.app.active_socket.recv(1024).decode()
            self.exercise_state_changed_signal.emit(response)
        except BlockingIOError:
            return None

    def send_stage_to_robot_with_phase(self, stage, exercise, score):
        index_of_phase = exercise.find("_fullfilled")
        start_index = index_of_phase + len("_fullfilled")
        number_str = exercise[start_index:]


        if score < 10:
            score = "0" + str(score)
        elif score >= 10:
            score = str(score)
        elif score < 0:
            score = "00"
        
        message = (score + exercise + "_" + stage)
        self.app.active_socket.sendall(message.encode())
         

    def send_stage_to_robot(self, stage, exercise, score):
        if score < 10:
            score = "0" + str(score)
        elif score >= 10:
            score = str(score)
        elif score < 0:
            score = "00"
            
        # send the stage to the robot
        print(score + stage )
        
        if stage == "up":
            message = (score + exercise + "_" + stage)
            self.app.active_socket.sendall(message.encode())
        elif stage == "down":
            message = (score + exercise + "_" + stage)
            self.app.active_socket.sendall(message.encode())
        elif stage == "warning":
            message = stage + '_' + exercise
            self.app.active_socket.sendall(message.encode())
        elif stage == "warning_corr":
            message = stage + '_' + exercise
            self.app.active_socket.sendall(message.encode())
        
        elif "fer" in stage:
            print("sending to robot")
            message = stage + '_' + exercise
            # if "_end" in stage:
            #     self.app.active_socket.sendall(self.messages["end_msg"].encode())
          
            self.app.active_socket.sendall(message.encode())
            

    def save_score(self, exercise_name):
        # save the time of saving, score and elapsed time to the .txt file
        with open("score.txt", "a") as file:
            file.write(str(datetime.now()) + " " + exercise_name + " " + self.ui.score_label.text() + " " + str(self.elapsed_time) + "\n")

    def update_exercise_label(self, note):
        # Update the label with the result of the exercise
        self.ui.note_label.setText(note)

    def start_timer(self):
        if self.timer_id is not None:
            self.app.killTimer(self.timer_id)
        self.timer_id = self.app.startTimer(1000)  # Starting a new timer