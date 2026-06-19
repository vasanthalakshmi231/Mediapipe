import cv2
import time

from src.hand_tracker import HandTracker
from src.frame_processor import FrameProcessor
from src.gesture_detector import GestureDetector
from src.virtual_mouse import VirtualMouse
from src.frame_saver import FrameSaver
from src.video_recorder import VideoRecorder


class CameraController:

    def __init__(self):

        # Create Objects
        self.processor = FrameProcessor()

        self.tracker = HandTracker(
            "models/hand_landmarker.task"
        )

        self.detector = GestureDetector()

        self.mouse = VirtualMouse()

        self.saver = FrameSaver()

        # Webcam
        self.cap = cv2.VideoCapture(0)

        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))

        # Video Recorder
        self.recorder = VideoRecorder(
            "saved_videos/output1.mp4",
            self.width,
            self.height
        )

        # Variables
        self.dragging = False

        self.last_click_time = 0
        self.click_delay = 0.5

        self.last_scroll_time = 0
        self.scroll_delay = 0.3

        self.prev_time = time.time()

    def run(self):

        while True:

            success, frame = self.cap.read()

            if not success:
                break

            frame = self.processor.resize_frame(frame)

            frame = self.processor.flip_frame(frame)

            frame = self.processor.blur_frame(frame)

            self.recorder.write_frame(frame)

            self.saver.save_frame(frame)

            result = self.tracker.detect(frame)

            h, w, _ = frame.shape

            if result.hand_landmarks:

                hand_landmarks = result.hand_landmarks[0]

                # -------------------------
                # Draw All Landmarks
                # -------------------------

                for landmark in hand_landmarks:

                    lx = int(landmark.x * w)
                    ly = int(landmark.y * h)

                    cv2.circle(
                        frame,
                        (lx, ly),
                        4,
                        (0, 255, 0),
                        -1
                    )

                # -------------------------
                # Cursor Movement
                # -------------------------

                index_tip = hand_landmarks[8]

                screen_x = int(
                    index_tip.x * self.mouse.screen_width
                )

                screen_y = int(
                    index_tip.y * self.mouse.screen_height
                )

                self.mouse.move_cursor(
                    screen_x,
                    screen_y
                )

                # Highlight index finger

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    10,
                    (0, 0, 255),
                    -1
                )

                current_time = time.time()

                # ====================================
                # LEFT CLICK
                # ====================================

                if self.detector.detect_click(hand_landmarks):

                    if current_time - self.last_click_time > self.click_delay:

                        self.mouse.left_click()

                        self.last_click_time = current_time

                    cv2.putText(
                        frame,
                        "LEFT CLICK",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                # ====================================
                # RIGHT CLICK
                # ====================================

                elif self.detector.detect_right_click(hand_landmarks):

                    if current_time - self.last_click_time > self.click_delay:

                        self.mouse.right_click()

                        self.last_click_time = current_time

                    cv2.putText(
                        frame,
                        "RIGHT CLICK",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        2
                    )

                # ====================================
                # DRAG
                # ====================================

                elif self.detector.detect_drag(hand_landmarks):

                    if not self.dragging:

                        self.mouse.drag_start()

                        self.dragging = True

                    cv2.putText(
                        frame,
                        "DRAGGING",
                        (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

                # ====================================
                # SCROLL
                # ====================================

                elif self.detector.detect_scroll(hand_landmarks):

                    if current_time - self.last_scroll_time > self.scroll_delay:

                        if y < h // 2:

                            self.mouse.scroll_up()

                        else:

                            self.mouse.scroll_down()

                        self.last_scroll_time = current_time

                    cv2.putText(
                        frame,
                        "SCROLL",
                        (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0),
                        2
                    )

                else:

                    if self.dragging:

                        self.mouse.drag_stop()

                        self.dragging = False

            # ====================================
            # FPS Counter
            # ====================================

            current_frame_time = time.time()

            fps = 1 / (current_frame_time - self.prev_time)

            self.prev_time = current_frame_time

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (500, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )


            # ====================================
            # Display
            # ====================================

            cv2.imshow(
                "Virtual Mouse",
                frame
            )


            # ====================================
            # ESC Key Exit
            # ====================================

            if cv2.waitKey(1) & 0xFF == 27:
                break


        # ====================================
        # Cleanup
        # ====================================

        self.cap.release()

        self.recorder.release()

        cv2.destroyAllWindows()