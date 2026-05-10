import mediapipe as mp
import math
import numpy as np


def remove_outliers(data):
        # Remove outliers using interquartile range
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        return [x for x in data if lower_bound <= x <= upper_bound]
    
def calculate_average(data):
    return sum(data) / len(data) if data else None

def calculate_angle_when_sitting(hip, knee, ankle):
        # Calculate the distance between the points
        a = math.sqrt((knee.x - ankle.x) ** 2 + (knee.y - ankle.y) ** 2 + (knee.z - ankle.z) ** 2)
        b = math.sqrt((hip.x - ankle.x) ** 2 + (hip.y - ankle.y) ** 2 + (hip.z - ankle.z) ** 2)
        c = math.sqrt((hip.x - knee.x) ** 2 + (hip.y - knee.y) ** 2 + (hip.z - knee.z) ** 2)
        
        angle = math.acos((c ** 2 + a ** 2 - b ** 2) / (2 * c * a))

        angle_degrees = math.degrees(angle)
        
        return angle_degrees


class SitPose():
    def __init__(self):
        self.distance_buffer_left_leg = []
        self.distance_buffer_right_leg = []

        self.buffer_left_leg_angle = []
        self.buffer_right_leg_angle = []

    
    def add_measurement_to_buffer_for_person_standing(self, left_leg_angle, right_leg_angle):
        if len(self.buffer_left_leg_angle) >= 4:
            self.buffer_left_leg_angle.pop(0)
        if len(self.buffer_right_leg_angle) >= 4:
            self.buffer_right_leg_angle.pop(0)

        self.buffer_left_leg_angle.append(left_leg_angle)
        self.buffer_right_leg_angle.append(right_leg_angle)


    def is_person_sitting(self, landmarks):
        left_hip_index = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
        left_knee_index = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
        left_ankle_index = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value
        right_hip_index = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
        right_knee_index = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
        right_ankle_index = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value

        if not all(landmarks.landmark[index].visibility > 0.5 if landmarks.landmark[index] else False for index in [left_hip_index, left_knee_index, left_ankle_index, right_hip_index, right_knee_index, right_ankle_index]):
            return "no_landmarks"

        left_leg_angle = calculate_angle_when_sitting(landmarks.landmark[left_hip_index], landmarks.landmark[left_knee_index], landmarks.landmark[left_ankle_index])
        right_leg_angle = calculate_angle_when_sitting(landmarks.landmark[right_hip_index], landmarks.landmark[right_knee_index], landmarks.landmark[right_ankle_index])

        self.add_measurement_to_buffer_for_person_standing(left_leg_angle, right_leg_angle)

        if len(self.buffer_left_leg_angle) < 4 or len(self.buffer_right_leg_angle) < 4:
            return

        filtered_left_leg_angles = remove_outliers(self.buffer_left_leg_angle)
        filtered_right_leg_angles = remove_outliers(self.buffer_right_leg_angle)
        average_left_leg_angle = calculate_average(filtered_left_leg_angles)
        average_right_leg_angle = calculate_average(filtered_right_leg_angles)

        if average_left_leg_angle is None or average_right_leg_angle is None:
            return "insufficient_data"
        else:
            pass

        sitting_angle_threshold = 90
        is_sitting = average_left_leg_angle < sitting_angle_threshold and average_right_leg_angle < sitting_angle_threshold

        self.buffer_left_leg_angle = []
        self.buffer_right_leg_angle = []

        return is_sitting
    

    def add_measurement_to_buffer(self, left_leg_measurement, right_leg_measurement):
        if len(self.distance_buffer_left_leg) >= 4:
            self.distance_buffer_left_leg.pop(0)
        if len(self.distance_buffer_right_leg) >= 4:
            self.distance_buffer_right_leg.pop(0)

        self.distance_buffer_left_leg.append(left_leg_measurement)
        self.distance_buffer_right_leg.append(right_leg_measurement)


    def is_person_standing(self, landmarks):
        left_hip_index = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
        left_knee_index = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
        right_hip_index = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
        right_knee_index = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value

        if not all(landmarks.landmark[index].visibility > 0.5 if landmarks.landmark[index] else False for index in [left_hip_index, left_knee_index, right_hip_index, right_knee_index]):
            return "no_landmarks"

        left_leg_distance = landmarks.landmark[left_knee_index].y - landmarks.landmark[left_hip_index].y
        right_leg_distance = landmarks.landmark[right_knee_index].y - landmarks.landmark[right_hip_index].y

        self.add_measurement_to_buffer(left_leg_distance, right_leg_distance)

        if len(self.distance_buffer_left_leg) < 1 or len(self.distance_buffer_right_leg) < 1:
            return
            # return "collecting_data"

        filtered_left_leg_distances = remove_outliers(self.distance_buffer_left_leg)
        filtered_right_leg_distances = remove_outliers(self.distance_buffer_right_leg)
        average_left_leg_distance = calculate_average(filtered_left_leg_distances)
        average_right_leg_distance = calculate_average(filtered_right_leg_distances)

        if average_left_leg_distance is None or average_right_leg_distance is None:
            return "insufficient_data"
        else:
            pass

        threshold = 0.20
        is_standing = average_left_leg_distance > threshold and average_right_leg_distance > threshold

        self.distance_buffer_left_leg = []
        self.distance_buffer_right_leg = []

        return is_standing
    
    def is_in_base_forefooting_position(self, landmarks, threshold_y=0.055):
   
        right_wrist =  landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y
        
        left_wrist = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y
        
      
        left_hip =  landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y
        
        left_knee = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y
        
        right_hip = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y
        
        right_knee = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y
        
        wrists_under_hips = ((right_wrist > right_hip - threshold_y) and 
                         (left_wrist > left_hip - threshold_y))
        
        is_base_position = wrists_under_hips
        return is_base_position
        
    

    