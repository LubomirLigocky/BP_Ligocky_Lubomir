# exercise_app_ui.py
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog
from PySide6.QtGui import QPixmap
from gui.menu import Ui_MainWindow
from gui.config_dialog import Ui_Dialog


class ExerciseAppUI(QMainWindow):

    

    def __init__(self, camera_thread, active_socket, base_speach_lang: dict = {}, json_config: dict = {}):
        super().__init__()

        # Store the camera thread
        self.camera_thread = camera_thread
        self.base_speach_lang = base_speach_lang
        self.json_config = json_config
        # Set up the UI
        self.ui = Ui_MainWindow()
        self.setup_ui(active_socket)

    def setup_ui(self, active_socket):
        self.ui.setupUi(self, active_socket, base_speach_lang=self.base_speach_lang, json_config=self.json_config)
        self.ui.score_label.setText("0")
        self.setStyleSheet("background-color: white;")
        self.showMaximized()
        not_started_exercise = self.base_speach_lang.get("exercise_phases", {}).get("not_launched", "Cvičenie ešte nezačalo")
        self.ui.note_label.setText(not_started_exercise)
        self.ui.distance_label.setText(" - ")

        # Set up camera thread connections
        # self.camera_thread.frame_captured.connect(self.update_camera)
        self.camera_thread.video_stream.connect(self.update_camera)
        self.camera_thread.update_distance_signal.connect(self.update_distance)
        

    # Set up button connections in the main app, not here    
    def show_dialog_config(self, input_config):
        config_dialog = QDialog(self)
        config_ui = Ui_Dialog()
        config_ui.setupUi(config_dialog, base_speach_lang=self.base_speach_lang)

        config_ui.accept_button.accepted.connect(config_dialog.accept)
        config_ui.accept_button.rejected.connect(config_dialog.reject)

        if input_config is not None:
            config_ui.serverIP_edit.setText(input_config['server_ip'])
            config_ui.serverPort_edit.setText(str(input_config['server_port']))
            config_ui.virtual_robot_ip.setText(input_config['virtual_robot_ip'])
            config_ui.physical_robot_ip.setText(input_config['physical_robot_ip'])
            config_ui.physical_checkBox.setChecked(input_config['is_physical'])
            config_ui.exercise_loop_input.setText(input_config['exercise_duration'])

            if input_config['target_gender'] == "female":
                config_ui.radioButton_female.setChecked(True)
            else:
                config_ui.radioButton_male.setChecked(True)

        result = config_dialog.exec()
        
        if result == QDialog.Accepted:

            if config_ui.radioButton_female.isChecked():
                radio_gender_button = "female"
            else:
                radio_gender_button = "male"
           
            config = {
                "server_ip": config_ui.serverIP_edit.text(),
                "server_port": config_ui.serverPort_edit.text(),
                "virtual_robot_ip": config_ui.virtual_robot_ip.text(),
                "physical_robot_ip": config_ui.physical_robot_ip.text(),
                "is_physical": config_ui.physical_checkBox.isChecked(),
                "enable_emotions": False,
                "lang": self.ui.lang_select.text(),
                "exercise_duration": config_ui.exercise_loop_input.text(),
                "target_gender": radio_gender_button,
                }

            return config
        
        return input_config
    

    def update_camera(self, qimage):
        self.ui.video_feed.setPixmap(QPixmap.fromImage(qimage))

    def update_distance(self, distance):
        self.ui.distance_label.setText(str(round(distance * 0.001, 2)) + " m")

    def update_score(self, score):
        self.ui.score_label.setText(str(score))
    
    def update_emotion(self, emotion):
        pass

    def update_note_label(self, text):
        self.ui.note_label.setText(text)

    def update_timer_label(self, elapsed_time):
        print("updating timer")
        self.ui.timer_label.setText(str(elapsed_time) + " s")

    def change_background_color(self, color):
        self.setStyleSheet(f"background-color: {color};")