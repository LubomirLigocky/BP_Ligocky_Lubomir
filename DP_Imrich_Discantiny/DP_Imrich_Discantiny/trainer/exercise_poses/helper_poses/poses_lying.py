import mediapipe as mp
import math
import numpy as np


def are_landmarks_aligned( landmarks, indices, axis='y', alignment_threshold=0.20):
    coordinates = [getattr(landmarks.landmark[index], axis) for index in indices if landmarks.landmark[index].visibility > 0.5]

    if not coordinates:
        return False

    coordinate_range = max(coordinates) - min(coordinates)

    return coordinate_range < alignment_threshold

def calculate_angle_leg_lifted_when_lying( hip, knee, ankle):
    horizontal = [hip[0] + 1, hip[1]]  # Point to the right of the hip, at the same y-coordinate
    
    # Calculate vectors
    vector_leg = [knee[0] - hip[0], knee[1] - hip[1]]
    
    vector_horizontal = [horizontal[0] - hip[0], horizontal[1] - hip[1]]
    
    # normalizovane vektory
    length_leg = math.hypot(*vector_leg)
    length_horizontal = math.hypot(*vector_horizontal)
    unit_leg = [vector_leg[0] / length_leg, vector_leg[1] / length_leg]
    unit_horizontal = [vector_horizontal[0] / length_horizontal, vector_horizontal[1] / length_horizontal]
    
    # uhol medzi dvoma vektormi
    dot_product = sum(a*b for a, b in zip(unit_leg, unit_horizontal))
    angle_rad = math.acos(dot_product)
    
    angle_deg = math.degrees(angle_rad)
    
    if knee[1] > hip[1]:
        angle_deg = 180 - angle_deg
    
    return angle_deg

class LyingPose():
    def __init__(self):
        self.right_knee_angle_buffer = []
        self.left_knee_angle_buffer = []

    def is_person_lying_on_floor_init(self, landmarks, alignment_threshold=0.20):
        leg_indices = [
            mp.solutions.pose.PoseLandmark.LEFT_HIP.value,
            mp.solutions.pose.PoseLandmark.RIGHT_HIP.value,
            mp.solutions.pose.PoseLandmark.LEFT_KNEE.value,
            mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value,
            mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value,
            mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value,
        ]

        leg_landmarks_visible = all(landmarks.landmark[index].visibility > 0.5 for index in leg_indices)

        if not leg_landmarks_visible:
            return False

        body_aligned_horizontally = are_landmarks_aligned(
            landmarks, 
            leg_indices,
            axis='y', 
            alignment_threshold=alignment_threshold
        )

        is_lying_down = body_aligned_horizontally

        return is_lying_down
    
    def is_leg_lifted(self, landmarks, hip_index, knee_index, ankle_index):
        hip = [landmarks.landmark[hip_index].x, landmarks.landmark[hip_index].y]
        knee = [landmarks.landmark[knee_index].x, landmarks.landmark[knee_index].y]
        ankle = [landmarks.landmark[ankle_index].x, landmarks.landmark[ankle_index].y]

        floor_point = [hip[0], ankle[1]]

        angle = calculate_angle_leg_lifted_when_lying(hip, knee, floor_point)

        if 70 <= angle <= 110:
            return True,0
        elif  angle < 70:
            return False, 1
        else:
            return False, 2
    

    def is_right_leg_lifted(self, landmarks):
        right_hip_index = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
        right_knee_index = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
        right_ankle_index = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value

        return self.is_leg_lifted(landmarks, right_hip_index, right_knee_index, right_ankle_index)


    def is_left_leg_lifted(self, landmarks):
        left_hip_index = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
        left_knee_index = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
        left_ankle_index = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value

        return self.is_leg_lifted(landmarks, left_hip_index, left_knee_index, left_ankle_index)
    

    def is_right_arm_lifted_when_lying(self, landmarks):
        right_shoulder_index = mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value
        right_wrist_index = mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value

        shoulder = landmarks.landmark[right_shoulder_index]
        wrist = landmarks.landmark[right_wrist_index]

        horizontal_vector = [1, 0]

        vertical_vector = [wrist.x - shoulder.x, wrist.y - shoulder.y]

        mag_vertical = math.sqrt(vertical_vector[0] ** 2 + vertical_vector[1] ** 2)
        unit_vertical = [vertical_vector[0] / mag_vertical, vertical_vector[1] / mag_vertical]

        dot_product = horizontal_vector[0] * unit_vertical[0] + horizontal_vector[1] * unit_vertical[1]

        angle_radians = math.acos(dot_product)

        angle_degrees = math.degrees(angle_radians)

        if 70 <= angle_degrees <= 110:
            return True,0
        elif  angle_degrees < 70:
            return False, 1
        else:
            return False, 2
    

    def is_left_arm_lifted_when_lying(self, landmarks):
        left_shoulder_index = mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value
        left_wrist_index = mp.solutions.pose.PoseLandmark.LEFT_WRIST.value

        shoulder = landmarks.landmark[left_shoulder_index]
        wrist = landmarks.landmark[left_wrist_index]

        floor_vector = [1, 0]

        arm_vector = [wrist.x - shoulder.x, wrist.y - shoulder.y]

        arm_vector_magnitude = math.sqrt(arm_vector[0]**2 + arm_vector[1]**2)
        arm_vector_normalized = [arm_vector[0] / arm_vector_magnitude, arm_vector[1] / arm_vector_magnitude]

        dot_product = floor_vector[0] * arm_vector_normalized[0] + floor_vector[1] * arm_vector_normalized[1]

        angle_radians = math.acos(dot_product)

        angle_degrees = math.degrees(angle_radians)

        if 70 <= angle_degrees <= 110:
            return True,0
        elif  angle_degrees < 70:
            return False, 1
        else:
            return False, 2