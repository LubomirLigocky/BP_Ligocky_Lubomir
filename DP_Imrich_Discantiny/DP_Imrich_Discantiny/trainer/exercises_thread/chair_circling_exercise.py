from .exercise import Exercise
import configuration.exercises as exercise_messages_configuration
from exercise_poses.chair_circling import ChairCirclingPose


class ChairCirclingExercise(Exercise):
    def __init__(self, messages, widget, app_instance):
        super(ChairCirclingExercise, self).__init__(messages, widget, app_instance)
        self.start_msg = messages['start_msg']

    def chair_circling_exercise(self):
        self.start_timer()

        self.camera_thread.current_exercise = ChairCirclingPose()

        self.camera_thread.frame_captured.connect(self.camera_thread.check_current_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_label)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot)

        self.camera_thread.exercise_interrupt_signal.connect(self.receive_msg_from_robot)
        self.exercise_state_changed_signal.connect(self.camera_thread.on_exercise_state_changed)