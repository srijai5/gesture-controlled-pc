import pyautogui
import numpy as np

def move_cursor(index_finger_tip, frame_size, screen_size):
    x = np.interp(index_finger_tip[0], [0, 1], [0, screen_size[0]])
    y = np.interp(index_finger_tip[1], [0, 1], [0, screen_size[1]])
    pyautogui.moveTo(x, y)

def detect_click(thumb_tip, index_tip):
    dist = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))
    if dist < 0.03:
        pyautogui.click()
