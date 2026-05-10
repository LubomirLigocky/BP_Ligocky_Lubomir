import mediapipe as mp
import math


class LegsPose():
    def __init__(self):
        pass

    def is_leg_visible(self, landmarks, hip_index, knee_index, ankle_index):
        landmarks_detected = all(landmark.visibility > 0.5 for landmark in [landmarks.landmark[hip_index], landmarks.landmark[knee_index], landmarks.landmark[ankle_index]])
        
        if landmarks_detected:
            hip = landmarks.landmark[hip_index]
            knee = landmarks.landmark[knee_index]
            ankle = landmarks.landmark[ankle_index]

            hip_knee_distance = math.hypot(hip.x - knee.x, hip.y - knee.y)
            knee_ankle_distance = math.hypot(knee.x - ankle.x, knee.y - ankle.y)

            min_distance_threshold = 0.02
            if hip_knee_distance > min_distance_threshold and knee_ankle_distance > min_distance_threshold:
                return True
        
        return False

    def is_left_leg_raised(self, landmarks):
        left_hip_index = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
        left_knee_index = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
        left_ankle_index = mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value

        if not self.is_leg_visible(landmarks, left_hip_index, left_knee_index, left_ankle_index):
            return "right_leg_not_visible_or_not_present"
        else:
            pass

        left_hip = [landmarks.landmark[left_hip_index].x, landmarks.landmark[left_hip_index].y]
        left_knee = [landmarks.landmark[left_knee_index].x, landmarks.landmark[left_knee_index].y]
        left_ankle = [landmarks.landmark[left_ankle_index].x, landmarks.landmark[left_ankle_index].y]

        is_raised = self.is_approximately_in_line(left_hip, left_knee, left_ankle)

        return is_raised
    

    def is_right_leg_raised(self, landmarks):
        right_hip_index = mp.solutions.pose.PoseLandmark.RIGHT_HIP.value
        right_knee_index = mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value
        right_ankle_index = mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value

        if not self.is_leg_visible(landmarks, right_hip_index, right_knee_index, right_ankle_index):
            return "right_leg_not_visible_or_not_present"
        else:
            pass

        right_hip = [landmarks.landmark[right_hip_index].x, landmarks.landmark[right_hip_index].y]
        right_knee = [landmarks.landmark[right_knee_index].x, landmarks.landmark[right_knee_index].y]
        right_ankle = [landmarks.landmark[right_ankle_index].x, landmarks.landmark[right_ankle_index].y]

        is_raised = self.is_approximately_in_line(right_hip, right_knee, right_ankle)

        return is_raised
    
    def is_approximately_in_line(self, hip, knee, ankle):
        vertical_movement_threshold_for_knee = -0.05  # Ak nastavim vyssiu hodnotu, musi viac zdvihnut (teda by sme sli nad nulu)
        vertical_movement_threshold_for_ankle = -0.23

        knee_lifted = (hip[1] - knee[1]) > vertical_movement_threshold_for_knee
        ankle_lifted = (hip[1] - ankle[1]) > vertical_movement_threshold_for_ankle

        horizontal_distance_threshold = 0.20 # Cim dame viac, tak tym je to benevolentnejsie, 0.25 je ked ma vyrovnanu nohu, cize 0.25 je vpodstate strop, ale tazko je to dobre vyladit
        horizontal_distance_of_knee_and_angle = abs(knee[1] - ankle[1])
        ankle_in_line_horizontally = horizontal_distance_of_knee_and_angle < horizontal_distance_threshold

        # Nakoniec sme neimplementovali vyrovnavanie nohy, cize netreba cekovat tie zvysne 2 veci, staci pozerat zdvihnutu nohu
        return  ankle_lifted