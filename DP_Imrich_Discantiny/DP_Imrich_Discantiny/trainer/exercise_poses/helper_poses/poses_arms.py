import mediapipe as mp
import math


class ArmsPose():

    def __init__(self):
        pass
        

    def arms_raised_up(self, landmarks, x_threshold=0.125):
        left_shoulder = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]

        right_shoulder = [landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y]

        left_arm_up = left_wrist[1] < left_shoulder[1] and abs(left_wrist[0] - left_shoulder[0]) < x_threshold
        right_arm_up = right_wrist[1] < right_shoulder[1] and abs(right_wrist[0] - right_shoulder[0]) < x_threshold

        return left_arm_up and right_arm_up

    

    def is_arms_in_line_for_lateral_raises(self, landmarks, vertical_threshold=0.10):
        shoulder_indices = [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow_indices = [mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist_indices = [mp.solutions.pose.PoseLandmark.LEFT_WRIST.value, mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        required_indices = shoulder_indices + elbow_indices + wrist_indices
        if not all(landmarks.landmark[index].visibility > 0.5 for index in required_indices):
            return False

        for shoulder_index, elbow_index, wrist_index in zip(shoulder_indices, elbow_indices, wrist_indices):
            shoulder = landmarks.landmark[shoulder_index]
            elbow = landmarks.landmark[elbow_index]
            wrist = landmarks.landmark[wrist_index]

            min_y = min(elbow.y, shoulder.y) - vertical_threshold
            max_y = max(elbow.y, shoulder.y) + vertical_threshold

            if not min_y <= wrist.y <= max_y:
                return False

        return True
    
    def is_hands_raised_in_sitting(self, landmarks):
        left_wrist_index = mp.solutions.pose.PoseLandmark.LEFT_WRIST.value
        right_wrist_index = mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value
        left_ear_index = mp.solutions.pose.PoseLandmark.LEFT_EAR.value
        right_ear_index = mp.solutions.pose.PoseLandmark.RIGHT_EAR.value

        if not all(landmarks.landmark[index].visibility > 0.5 for index in [left_wrist_index, right_wrist_index, left_ear_index, right_ear_index]):
            return False

        left_wrist_y = landmarks.landmark[left_wrist_index].y
        right_wrist_y = landmarks.landmark[right_wrist_index].y
        left_ear_y = landmarks.landmark[left_ear_index].y
        right_ear_y = landmarks.landmark[right_ear_index].y

        minimum_clearance = 0.05

        hands_raised_strictly = (left_wrist_y + minimum_clearance) < left_ear_y and (right_wrist_y + minimum_clearance) < right_ear_y

        return hands_raised_strictly
    

    def is_arms_put_down(self, landmarks, y_treshold):

        shoulder_indices = [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow_indices = [mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist_indices = [mp.solutions.pose.PoseLandmark.LEFT_WRIST.value, mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        required_indices = shoulder_indices + elbow_indices + wrist_indices
        
        if not all(landmarks.landmark[index].visibility > 0.5 for index in required_indices):
            return False

        for shoulder_index, elbow_index, wrist_index in zip(shoulder_indices, elbow_indices, wrist_indices):
            shoulder = landmarks.landmark[shoulder_index]
            elbow = landmarks.landmark[elbow_index]
            wrist = landmarks.landmark[wrist_index]

            if wrist.y < shoulder.y + y_treshold:
                return False

            if elbow.y < shoulder.y + y_treshold:
                return False

            if wrist.y < elbow.y + y_treshold:
                return False

        return True
    
    def wrong_tpose_pose_warning(self, arm_coordinates):
        # Extract x-coordinates of shoulders and wrists from the coordinates dictionary
        left_shoulder_y = arm_coordinates["left_shoulder"][1]
        right_shoulder_y = arm_coordinates["right_shoulder"][1]
        left_wrist_y = arm_coordinates["left_wrist"][1]
        right_wrist_y = arm_coordinates["right_wrist"][1]

        # Determine if wrists are "above" or "below" shoulders in x-coordinate
        left_wrist_above_shoulder = left_wrist_y < left_shoulder_y
        right_wrist_above_shoulder = right_wrist_y < right_shoulder_y

        if left_wrist_above_shoulder and right_wrist_above_shoulder:
            return "tpose_arms_above"
        elif not left_wrist_above_shoulder and not right_wrist_above_shoulder:
            return "tpose_arms_below"
        else:
            return "tpose_arms_wrong"
    
    def wrong_arms_pose_warning(self, exercise_name, arms, exercise, width_threshold):

        both_arms = True
        print(arms)
        if arms["left"] == None or arms["right"] == None:
           return "Chyba"

        if arms["left"]["coordinates"] == None or arms["right"]["coordinates"] == None:
           both_arms = False

        # print("arms:", arms, "Both_arms:", both_arms)

        height_threshold = 0.05
        side_arm = None

        right_arm_up = False
        left_arm_up = False

        right_arm_low = False
        left_arm_low = False

        right_arm_aside = False
        left_arm_aside = False
        
        for side, status in arms.items():
            if status["coordinates"] is not None:
                side_arm = side
                wrist_too_high =  False
                wrist_too_low =  False

                shoulder_x, shoulder_y = status["coordinates"]["shoulder"]
                wrist_x, wrist_y = status["coordinates"]["wrist"]
                
                if wrist_y < shoulder_y - height_threshold:
                    wrist_too_high =  True
                    print(f"Warning: {side.capitalize()} wrist is too high for {exercise_name}.")
                
                elif wrist_y > shoulder_y + height_threshold:
                    wrist_too_low =  True
                    print(f"Warning: {side.capitalize()} wrist is too low for {exercise_name}.")
                
                if side == "right":
                    if wrist_too_high:
                        right_arm_up = True

                    elif wrist_too_low:
                        right_arm_low = True
                    
                    if wrist_x < shoulder_x - width_threshold:
                        right_arm_aside = True
                        print(f"Warning: Right wrist is too far right from the right shoulder.", wrist_x, shoulder_x)
                
                    # if elbow_x > shoulder_x :
                    #     print(f"Warning: Right elbow is too far right from the right shoulder.")

                elif side == "left":
                    if wrist_too_high:
                        left_arm_up = True

                    elif wrist_too_low:
                        left_arm_low = True
                    
                    if wrist_x > shoulder_x + width_threshold:
                        left_arm_aside = True
                        print(f"Warning: Left wrist is too far left from the left shoulder.", wrist_x, shoulder_x)
                    # if elbow_x < shoulder_x:
                    #     print(f"Warning: Left elbow is too far left from the left shoulder.")
            
        return exercise.warning_message(both_arms, side_arm, right_arm_up, left_arm_up, right_arm_low,left_arm_low, right_arm_aside, left_arm_aside)
    
    def is_arms_raised_forward(self, landmarks, width_threshold, height_threshold=0.16, vertical_offset= 0.085 ):
        shoulder_indices = [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow_indices = [mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist_indices = [mp.solutions.pose.PoseLandmark.LEFT_WRIST.value, mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        required_indices = shoulder_indices + elbow_indices + wrist_indices

        # Check if all landmarks are sufficiently visible
        if not all(landmarks.landmark[index].visibility > 0.5 for index in required_indices):
            return False, {"left": None, "right": None}

        arms_status = {
            "left": {"coordinates": None},
            "right": {"coordinates": None}
        }

        for side, (shoulder_index, elbow_index, wrist_index) in zip(["left", "right"], zip(shoulder_indices, elbow_indices, wrist_indices)):
            shoulder = landmarks.landmark[shoulder_index]
            elbow = landmarks.landmark[elbow_index]
            wrist = landmarks.landmark[wrist_index]

            left_bound = shoulder.x - width_threshold 
            right_bound = shoulder.x + width_threshold 
            top_bound = shoulder.y - height_threshold
            bottom_bound = shoulder.y + vertical_offset

             # Check if both elbow and wrist are within the rectangle
            if (left_bound <= elbow.x <= right_bound and top_bound <= elbow.y <= bottom_bound and
                left_bound <= wrist.x <= right_bound and top_bound <= wrist.y <= bottom_bound):
               continue
            
            # print(side, top_bound, bottom_bound, "shoulder", shoulder.x)
            
            arms_status[side]["coordinates"] = {
                    "shoulder": (shoulder.x, shoulder.y),
                    "elbow": (elbow.x, elbow.y),
                    "wrist": (wrist.x, wrist.y)
                }

        
        if arms_status["left"]["coordinates"] or arms_status["right"]["coordinates"]:
            return False, arms_status

        return True, arms_status
 

    def is_arms_in_tpose(self, landmarks, y_threshold, wrist_distance_threshold):
        left_shoulder = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        is_left_elbow_aligned = abs(left_elbow.y - left_shoulder.y) < y_threshold
        is_right_elbow_aligned = abs(right_elbow.y - right_shoulder.y) < y_threshold
        is_left_wrist_aligned = abs(left_wrist.y - left_shoulder.y) < y_threshold
        is_right_wrist_aligned = abs(right_wrist.y - right_shoulder.y) < y_threshold

        def calculate_distance(point1, point2, wrist_distance_threshold):
            distance =  math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
            return distance < wrist_distance_threshold

        is_left_wrist_close = calculate_distance(left_wrist, left_shoulder, wrist_distance_threshold)
        is_right_wrist_close = calculate_distance(right_wrist, right_shoulder, wrist_distance_threshold)

        in_tpose = (is_left_elbow_aligned and is_right_elbow_aligned and 
                    is_left_wrist_aligned and is_right_wrist_aligned and 
                    not is_left_wrist_close and not is_right_wrist_close)

        coordinates = {
            "left_shoulder": (left_shoulder.x, left_shoulder.y),
            "right_shoulder": (right_shoulder.x, right_shoulder.y),
            "left_wrist": (left_wrist.x, left_wrist.y),
            "right_wrist": (right_wrist.x, right_wrist.y)
        }

        # Return the T-pose boolean and the coordinates dictionary
        return in_tpose, coordinates, (is_left_wrist_close or is_right_wrist_close)