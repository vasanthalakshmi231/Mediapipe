#from utils import calculate_distance
from src.utils import calculate_distance


class GestureDetector:

    def __init__(self):

        self.click_threshold = 0.05

    # Left Click
    def detect_click(
            self,
            hand_landmarks):

        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]

        distance = calculate_distance(
            thumb_tip,
            index_tip
        )

        return distance < self.click_threshold

    # Right Click
    def detect_right_click(
            self,
            hand_landmarks):

        thumb_tip = hand_landmarks[4]
        middle_tip = hand_landmarks[12]

        distance = calculate_distance(
            thumb_tip,
            middle_tip
        )

        return distance < self.click_threshold

    # Drag Gesture
    def detect_drag(
            self,
            hand_landmarks):

        thumb_tip = hand_landmarks[4]
        ring_tip = hand_landmarks[16]

        distance = calculate_distance(
            thumb_tip,
            ring_tip
        )

        return distance < self.click_threshold

    # Scroll Gesture
    def detect_scroll(
        self,
        hand_landmarks):

        thumb_tip = hand_landmarks[4]
        pinky_tip = hand_landmarks[20]

        distance = calculate_distance(
            thumb_tip,
            pinky_tip
        )

        return distance < self.click_threshold