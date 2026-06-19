import pyautogui


class VirtualMouse:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        self.prev_x = 0
        self.prev_y = 0

        self.smoothing = 5

    def move_cursor(self, x, y):

        curr_x = self.prev_x + (x - self.prev_x) / self.smoothing

        curr_y = self.prev_y + (y - self.prev_y) / self.smoothing

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x = curr_x
        self.prev_y = curr_y

    def left_click(self):

        pyautogui.click()

    def right_click(self):

        pyautogui.rightClick()

    def drag_start(self):

        pyautogui.mouseDown()

    def drag_stop(self):

        pyautogui.mouseUp()

    def scroll_up(self):

        pyautogui.scroll(50)

    def scroll_down(self):

        pyautogui.scroll(-50)