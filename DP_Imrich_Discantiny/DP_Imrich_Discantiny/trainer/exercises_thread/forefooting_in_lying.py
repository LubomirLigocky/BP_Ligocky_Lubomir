from .exercise import Exercise
import configuration.exercises as exercise_messages_configuration

class ForefootingInLying(Exercise):
    def __init__(self, messages, widget, app_instance):
        super(ForefootingInLying, self).__init__(messages, widget, app_instance)
        self.start_msg = messages['start_msg'] + ","

    def forefooting_in_lying_exercise(self):
        self.start_timer()
        self.camera_thread.frame_captured.connect(self.camera_thread.check_forefooting_in_lying_exercise)
        self.camera_thread.exercise_label_signal.connect(self.update_label)
        self.camera_thread.stage_signal.connect(self.send_stage_to_robot_with_phase)

    # # def increment_score(self, exercise_name, increment_score_bool):
    # #     print("aabbcc")
    # def exercise_update_score(self, exercise_name, increment_score=False):
    #     # if increment_score:
    #     print("asd222")
    #     self.increment_score()
    #     # Additional logic for updating scores based on specific exercises can be added here

    # def increment_score(self):
    #     self.score += 1  # Increment the score by 1
    #     print(f"Score incremented to: {self.score}")
    #     # You might also want to update any UI elements or perform other actions as a result of the score change here