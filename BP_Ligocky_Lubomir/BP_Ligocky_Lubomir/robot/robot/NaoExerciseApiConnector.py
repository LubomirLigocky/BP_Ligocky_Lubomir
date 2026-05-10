import socket

from robot._exercises_impl.forefooting_predpazovanie import ForefootingPredpazovanie


class NaoExerciseApiConnector:
    HOST = ""
    PORT = 9559  # 52939 #9559 #config_robot.PORT_SERVER
    print(HOST)
    print(PORT)
    zakladne_cviky_bez_queue = ["tpose", "right_leg", "left_leg", "squat", "arm_circling", "arm_sit_circling",
                                "chair_circling"]

    score = 0
    score_size = 2
    use_queue = True

    warningStart = 'ExerciseContinue_'

    def __init__(self):
        print("Init connection...")

        self.naoqi_instance = None

        self.my_socket = socket.socket()

        print(self.HOST)
        self.my_socket.bind((self.HOST, self.PORT))
        self.my_socket.listen(5)
        self.conn, self.addr = self.my_socket.accept()
        self.curr_exercise = None


    def predpazovanie(self):
        self.score = 0
        message = message[self.score_size:]
        score = int(self.score)

        print(message, score)
        # self.say_score(score)


        self.curr_exercise = ForefootingPredpazovanie(self.naoqi_instance)
        self.curr_exercise.run_exercise(self.score, message, self.conn)