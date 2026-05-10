from .exercise import Exercise
import configuration.exercises as exercise_messages_configuration

class SadanieNaStolicku(Exercise):
    def __init__(self, messages, widget, app_instance):
        super(SadanieNaStolicku, self).__init__(messages, widget, app_instance)
        self.start_msg = messages['start_msg'] + ","

    def sadanie_na_stolicku_exercise(self):
        self.start_timer()
        self.camera_thread.frame_captured.connect(self.camera_thread.check_sadanie_na_stolicku_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_label)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot_with_phase)