from typing import List, Optional

import numpy as np
import mediapipe as mp
import math

from side_camera import SideCamera


class ArmsPose():

    def __init__(self):
        pass
        

    def arms_raised_up(self, landmarks, x_threshold=0.125, above_arms: bool = False, y_threshold: float = 10):
        if not landmarks:
            print("No Landmarks (arms_raised_up)")
            return False
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

        left_arm_up = left_wrist[1] < left_shoulder[1] and abs(left_wrist[0] - left_shoulder[0]) < x_threshold and (not above_arms or abs(left_wrist[1] - left_shoulder[1]) > y_threshold)
        right_arm_up = right_wrist[1] < right_shoulder[1] and abs(right_wrist[0] - right_shoulder[0]) < x_threshold and (not above_arms or abs(right_wrist[1] - right_shoulder[1]) > y_threshold)

        print("TEST")
        print(left_wrist[1] - left_shoulder[1])
        print(right_wrist[1] - right_shoulder[1])
        return left_arm_up and right_arm_up


    def is_arms_in_line_for_lateral_raises(self, landmarks, vertical_threshold=0.10):
        if not landmarks:
            print("No Landmarks (is_arms_in_line_for_lateral_raises)")
            return False
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
        if not landmarks:
            print("No Landmarks (is_hands_raised_in_sitting)")
            return False
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
        if not landmarks:
            print("No Landmarks (is_arms_put_down)")
            return False
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
        front_or_back = "front"
        for side, status in arms.items():
            if status["coordinates"] is not None:
                side_arm = side
                wrist_too_high =  False
                wrist_too_low =  False

                shoulder_x, shoulder_y = status["coordinates"]["shoulder"]
                front_or_back = status["coordinates"]["front_or_back"]
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

        return exercise.warning_message(both_arms, side_arm, right_arm_up, left_arm_up, right_arm_low,left_arm_low, right_arm_aside, left_arm_aside, front_or_back)


    def is_arms_raised_forward(self, landmarks, width_threshold, height_threshold=0.16, vertical_offset= 0.085,
                               side_camera: Optional[SideCamera] = None, depth: List = None, frame = None):
        def check_side_position_depth_camera():
            nose = landmarks.landmark[nose_index]
            left_index = landmarks.landmark[19]
            left_pinky = landmarks.landmark[17]
            right_index = landmarks.landmark[20]
            right_pinky = landmarks.landmark[18]
            hip = landmarks.landmark[24]
            print("Nose: " + str(nose.z))
            print("SHOULDERRRRRRRRRRRRRR")
            print("x: " + str(wrist.x))
            print("y: " + str(wrist.y))
            print("z: " + str(wrist.z))
            # front_or_back = "front" if abs(wrist.z) - abs(nose.z) < 0.05 or wrist.z < 0.05 else "back"

            nose_wrist_comparison, nose_depth, left_index_depth = self.compare_based_on_average_depth(landmarks, left_index, depth, frame, hip)
            front_or_back ="front" if not left_index_depth or nose_depth + 70 >= left_index_depth else "back"
            if not left_index_depth or front_or_back == "back":
                print("PINKY")
                nose_wrist_comparison, nose_depth, left_pinky_depth = self.compare_based_on_average_depth(landmarks,
                                                                                                          left_pinky,
                                                                                                          depth, frame
                                                                                                          , hip)
                front_or_back = "front" if not left_pinky_depth or nose_depth + 70 >= left_pinky_depth else "back"
                if not left_index_depth or front_or_back == "back":
                    print("WRIST")
                    nose_wrist_comparison, nose_depth, wrist_depth = self.compare_based_on_average_depth(landmarks, wrist, depth,
                                                                                                  frame, nose)
                    front_or_back = "front" if not wrist_depth or nose_depth + 50 >= wrist_depth else "back"
                    if not wrist_depth or front_or_back == "back":
                        print("ELBOW")
                        nose_elbow_comparison, nose_depth, elbow_depth = self.compare_based_on_average_depth(landmarks, elbow,
                                                                                                     depth,
                                                                                                     frame, nose)
                        front_or_back = "front" if not elbow_depth or nose_depth + 50 >= elbow_depth else "back"

                        if not elbow_depth or front_or_back == "back":
                            print("PINKY")
                            nose_wrist_comparison, nose_depth, left_pinky_depth = self.compare_based_on_average_depth(landmarks, left_pinky,
                                                                                                              depth, frame, nose)
                            front_or_back = "front" if not left_pinky_depth or nose_depth + 50 >= left_pinky_depth else "back"
                            print("left pinky: " + str(left_pinky_depth))
                            if not left_pinky_depth or front_or_back == "back":
                                print("PINKY")
                                nose_wrist_comparison, nose_depth, right_pinky_depth = self.compare_based_on_average_depth(landmarks,
                                                                                                                  right_pinky,
                                                                                                                  depth,
                                                                                                                  frame,
                                                                                                                  nose)
                                front_or_back = "front" if not right_pinky_depth or nose_depth + 50 >= right_pinky_depth  else "back"
                                print("right pinky: " + str(right_pinky_depth ))
                                if not right_pinky_depth or front_or_back == "back":
                                    print("PINKY")
                                    nose_wrist_comparison, nose_depth, right_index_depth = self.compare_based_on_average_depth(
                                        landmarks,
                                        right_index,
                                        depth,
                                        frame,
                                        nose)
                                    front_or_back = "front" if not right_index_depth or nose_depth + 50 >= right_index_depth else "back"
                                    print("right_index: " + str(right_index_depth))

            print("Nose: " + str(nose_wrist_comparison))
            print("Nose depth: " + str(nose_depth))
            #print("Wrist depth: " + str(wrist_depth))
            #print("Shoulder depth: " + str(hip_depth))
            print("left index: " + str(left_index_depth))

            print(front_or_back)
            return front_or_back

        def check_side_position_side_camera(side_camera: SideCamera):
            nose_landmarks = landmarks.landmark[nose_index]
            left_index_landmarks = landmarks.landmark[19]
            right_index_landmarks = landmarks.landmark[20]

            if not side_camera.process_input_and_check_on_exceeding(left_index_landmarks, nose_landmarks):
                return "back"
            if not side_camera.process_input_and_check_on_exceeding(right_index_landmarks, nose_landmarks):
                return "back"
            return "front"

        if not landmarks:
            print("No Landmarks (is_arms_raised_forward)")
            return False
        shoulder_indices = [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow_indices = [mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist_indices = [mp.solutions.pose.PoseLandmark.LEFT_WRIST.value, mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

        
        left_wrist_index = 15
        right_wrist_index = 16
        left_elbow_index = 13
        right_elbow_index = 14
        nose_index = 0

        left_w_visible = landmarks.landmark[left_wrist_index].visibility > 0.5
        right_w_visible = landmarks.landmark[right_wrist_index].visibility > 0.5
        left_e_visible = landmarks.landmark[left_elbow_index].visibility > 0.5
        right_e_visible = landmarks.landmark[right_elbow_index].visibility > 0.5

        if not (left_w_visible and right_w_visible):
            wrist_indices = [mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]

        elif not (left_e_visible and right_e_visible): 
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


            if side_camera:
                front_or_back = check_side_position_side_camera(side_camera)
            else:
                front_or_back = "front" # check_side_position_depth_camera() #does not work properly
             # Check if both elbow and wrist are within the rectangle
            if front_or_back == "front" and left_bound <= wrist.x <= right_bound and top_bound <= wrist.y <= bottom_bound:
                continue
            #if left_bound <= wrist.x <= right_bound and top_bound <= wrist.y <= bottom_bound:
            #    continue
            # print(side, top_bound, bottom_bound, "shoulder", shoulder.x)
            arms_status[side]["coordinates"] = {
                "shoulder": (shoulder.x, shoulder.y),
                "front_or_back": front_or_back,
                "elbow": (elbow.x, elbow.y),
                "wrist": (wrist.x, wrist.y)
            }

        if arms_status["left"]["coordinates"] or arms_status["right"]["coordinates"]:
            return False, arms_status

        return True, arms_status
 

    def is_arms_in_tpose(self, landmarks, y_threshold, wrist_distance_threshold):
        if not landmarks:
            print("No Landmarks (is_arms_in_tpose)")
            return False
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

    def compare_based_on_depth(self, landmarks, landmark_to_compare, depth, frame, baseline_landmarks = None):
        if not baseline_landmarks:
            baseline_landmarks = landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value]
        if baseline_landmarks.visibility < 0.65 and landmark_to_compare.visibility < 0.65:
            return None, None, None

        baseline_coords = [baseline_landmarks.x, baseline_landmarks.y]

        frame_width, frame_height = frame.shape[1], frame.shape[0]
        baseline_coordinates = tuple(
            np.multiply(baseline_coords, [frame_width, frame_height]).astype(int))

        # Ensure coordinates are within the bounds of the 'depth' array
        baseline_coordinates = (
            min(baseline_coordinates[0], frame_width - 1),
            min(baseline_coordinates[1], frame_height - 1)
        )

        target_coords = [landmark_to_compare.x, landmark_to_compare.y]
        target_coordinates = tuple(
            np.multiply(target_coords, [frame_width, frame_height]).astype(int))

        # Ensure coordinates are within the bounds of the 'depth' array
        target_coordinates = (
            min(target_coordinates[0], frame_width - 1),
            min(target_coordinates[1], frame_height - 1)
        )
        # Get the distance value from the 'depth' array using the nose coordinates
        #if frame_width < 1920:
        baseline_distance = depth[baseline_coordinates[1], baseline_coordinates[0]]
        target_distance = depth[target_coordinates[1], target_coordinates[0]]
        return target_distance - baseline_distance, baseline_distance, target_distance


    def count_average_per_rect(self, depth, point_coordinates, rect_width, frame):
        item_count = 1
        overall_count = 0
        frame_width, frame_height = frame.shape[1], frame.shape[0]

        location_coordinates = tuple(
            np.multiply(point_coordinates, [frame_width, frame_height]).astype(int))

        # Ensure coordinates are within the bounds of the 'depth' array
        location_coordinates = (
            min(location_coordinates[0], frame_width - 1),
            min(location_coordinates[1], frame_height - 1)
        )
        location_y, location_x = location_coordinates[1], location_coordinates[0]
        print("Location [" + str(location_x) + "  " + str(location_y))
        for y in range(int(location_y - rect_width / 2), int(location_y + rect_width / 2), 1):
            if y > 0:
                for x in range(int(location_x - rect_width / 2), int(location_x + rect_width / 2), 1):
                    if x > 0:
                        if observed_depth := depth[y, x]:
                            item_count += 1
                            overall_count += observed_depth
        average = overall_count / item_count
        return average


    def count_maximum_per_rect(self, depth, point_coordinates, rect_width, frame):
        maximum = 500000000000
        frame_width, frame_height = frame.shape[1], frame.shape[0]

        location_coordinates = tuple(
            np.multiply(point_coordinates, [frame_width, frame_height]).astype(int))

        # Ensure coordinates are within the bounds of the 'depth' array
        location_coordinates = (
            min(location_coordinates[0], frame_width - 1),
            min(location_coordinates[1], frame_height - 1)
        )
        location_y, location_x = location_coordinates[1], location_coordinates[0]
        print("Location [" + str(location_x) + "  " + str(location_y))
        for y in range(int(location_y - rect_width / 2), int(location_y + rect_width / 2), 1):
            if y > 0 and y < 1920:
                for x in range(int(location_x - rect_width / 2), int(location_x + rect_width / 2), 1):
                    if x > 0 and x < 1920:
                        print(depth[y, x])
                        if observed_depth := depth[y, x]:
                            maximum = max(maximum, observed_depth)
        if maximum == 500000000000:
            return None
        return maximum


    def compare_based_on_average_depth(self, landmarks, landmark_to_compare, depth, frame, baseline_landmarks = None):
        if not baseline_landmarks:
            baseline_landmarks = landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value]
        if baseline_landmarks.visibility < 0.35 and landmark_to_compare.visibility < 0.35:
            return None, None, None

        baseline_coords = [baseline_landmarks.x, baseline_landmarks.y]
        #frame_width, frame_height = frame.shape[1], frame.shape[0]
        target_coords = [landmark_to_compare.x, landmark_to_compare.y]

        # Get the distance value from the 'depth' array using the nose coordinates
        #if frame_width < 1920:
        baseline_distance = self.count_average_per_rect(depth, baseline_coords, 20, frame)
        target_distance = self.count_average_per_rect(depth, target_coords, 20, frame)
        return target_distance - baseline_distance, baseline_distance, target_distance


    def compare_based_on_maximal_depth(self, landmarks, landmark_to_compare, depth, frame, baseline_landmarks = None):
        if not baseline_landmarks:
            baseline_landmarks = landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value]
        if baseline_landmarks.visibility < 0.65 and landmark_to_compare.visibility < 0.65:
            return None, None, None

        baseline_coords = [baseline_landmarks.x, baseline_landmarks.y]
        #frame_width, frame_height = frame.shape[1], frame.shape[0]
        target_coords = [landmark_to_compare.x, landmark_to_compare.y]

        # Get the distance value from the 'depth' array using the nose coordinates
        #if frame_width < 1920:
        baseline_distance = self.count_maximum_per_rect(depth, baseline_coords, 20, frame)
        target_distance = self.count_maximum_per_rect(depth, target_coords, 30, frame)
        return target_distance - baseline_distance, baseline_distance, target_distance
