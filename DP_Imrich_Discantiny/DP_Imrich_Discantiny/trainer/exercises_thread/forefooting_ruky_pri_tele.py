from .exercise import Exercise
import configuration.exercises as exercise_messages_configuration

class ForefootingRukyPriTele(Exercise):
    def __init__(self, messages, widget, app_instance):
        super(ForefootingRukyPriTele, self).__init__(messages, widget, app_instance)
        self.start_msg = messages['start_msg'] + ","

    def forefooting_ruky_pri_tele_exercise(self):
        self.start_timer()
        self.camera_thread.frame_captured.connect(self.camera_thread.check_forefooting_ruky_pri_tele_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_label)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot_with_phase)