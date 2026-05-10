from exercise_poses.predpazovanie_exercise import PredpazovanieExercisePose
from .exercise import Exercise
import configuration.exercises as exercise_messages_configuration

class Predpazovanie(Exercise):

    def __init__(self, messages, widget, app_instance):
        super(Predpazovanie, self).__init__(messages, widget, app_instance)
        self.start_msg = messages['start_msg'] + ","

    def predpazovanie_exercise(self):
        self.start_timer()

        self.camera_thread.current_exercise = PredpazovanieExercisePose()
        self.camera_thread.frame_captured.connect(self.camera_thread.check_current_exercise)

        self.camera_thread.exercise_label_signal.connect(self.update_label)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot_with_phase)

        self.camera_thread.exercise_interrupt_signal.connect(self.receive_msg_from_robot)
        self.exercise_state_changed_signal.connect(self.camera_thread.on_exercise_state_changed)
