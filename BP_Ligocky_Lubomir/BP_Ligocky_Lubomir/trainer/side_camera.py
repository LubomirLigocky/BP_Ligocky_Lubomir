import traceback
import asyncio

import cv2
import numpy as np
import mediapipe as mp
import winrt.windows.devices.enumeration as windows_devices
from PySide6.QtCore import QThread


async def get_camera_info():
    return await windows_devices.DeviceInformation.find_all_async()


class SideCamera:
    CAMERA_NAME = "MX Brio"

    def __init__(self):
        # Set up the Mediapipe pose estimation
        self.mp_pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.disabled = True
        self.last_stored_frame = None

    def connect_camera(self, camera_name: str = CAMERA_NAME, frame_size: tuple = (3840, 2160) ):
        connected_cameras = asyncio.run(get_camera_info())
        names = [camera.name for camera in connected_cameras]
        self.usb_brio_input = None
        # for i, device_name in enumerate(device_list):
        #   print(f"opencv_index: {i}, device_name: {device_name}")
        if camera_name not in names:
            print("Camera not found!")
            self.usb_brio_input = None
            self.disabled = True
        else:
            self.disabled = False
            self.usb_brio_input = names.index(camera_name)

            #self.cap = cv2.VideoCapture(self.usb_brio_input)
            #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size[0])
            #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size[1])
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            print(self.usb_brio_input)
            print(cv2.CAP_AVFOUNDATION)
            #for Windows cv2.CAP_DSHOW
            self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)


    def process_input(self):
        ret_webcam, brio_frame = self.cap.read()
        if self.cap.isOpened():
            brio_frame = cv2.resize(brio_frame, (1280, 720), fx=1.25, fy=1.25, interpolation=cv2.INTER_CUBIC)
            # if width == 1920:
            #     frame_np = np.array(frame.data, dtype=np.uint8)  # Convert to NumPy array
            #     frame = cv2.resize(frame_np, (1280, 720))  # Resize

            return brio_frame
        else:
            print("Frame is broken. Try update VideoCapture mode")
        return None
    # h, w = brio_frame.shape[:2]
    # blob = cv2.dnn.blobFromImage(brio_frame, 1.0, (300, 300),
    #                             (104.0, 177.0, 123.0), False, False)
    # bytes_per_line = 3 * width
    # Convert to QImage and emit the signal
    # qimage = QImage(brio_frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
    # self.frame_captured.emit(qimage, self.fer.domimant_em_text)
    def process_input_and_check_on_exceeding(self, landmark_to_compare, baseline_landmarks=None):
        #if self.last_stored_frame:
        #    ret_webcam, brio_frame = self.last_stored_frame
        #else:
        brio_frame = self.process_input()
        brio_frame = cv2.resize(brio_frame, (1280, 720), interpolation=cv2.INTER_AREA)  # Resize
        # height, width, channel = brio_frame.shape
        results = self.mp_pose.process(brio_frame)
        # print("results",results.pose_landmarks)
        landmarks = results.pose_landmarks
        is_exceeding = self.is_exceeding_based_on_position(landmarks, landmark_to_compare, brio_frame,
                                                           baseline_landmarks=baseline_landmarks, threshold=250)
        print("RESSUULLT");
        print(is_exceeding)
        return is_exceeding

    def is_exceeding_based_on_position(self, landmarks, landmark_to_compare, frame,
                                       baseline_landmarks=None, threshold: float=0.0):
        resulting_comparison, baseline_coordinates, target_coordinates = self.evaluation_based_on_position(
            landmarks, landmark_to_compare, frame, baseline_landmarks)
        print(target_coordinates[0])
        print(baseline_coordinates[0])
        if target_coordinates[0] > baseline_coordinates[0] + threshold:
            return False
        return True

    def evaluation_based_on_position(self, landmarks, landmark_to_compare, frame, baseline_landmarks = None):
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
        resulting_comparison = [target_coordinates[0] - baseline_coordinates[0], target_coordinates[1] - baseline_coordinates[1]]
        return resulting_comparison, baseline_coordinates, target_coordinates
