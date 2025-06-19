import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

# Variables to help smooth cursor movement
prev_x, prev_y = 0, 0
smoothening = 7

def fingers_up(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if landmarks[4][0] < landmarks[3][0] else 0)

    # Other fingers
    for id in range(1, 5):
        fingers.append(1 if landmarks[tips_ids[id]][1] < landmarks[tips_ids[id] - 2][1] else 0)

    return fingers

def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

cap = cv2.VideoCapture(0)

click_delay = 0.3
last_click_time = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get landmark positions in pixels
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append((int(lm.x * w), int(lm.y * h)))

        # Normalize landmarks for gesture logic (0-1)
        norm_landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

        fingers = fingers_up(norm_landmarks)

        # Move cursor if open palm (all fingers up)
        if fingers == [1, 1, 1, 1, 1]:
            x = landmarks[8][0]
            y = landmarks[8][1]

            # Smooth cursor
            curr_x = prev_x + (x - prev_x) / smoothening
            curr_y = prev_y + (y - prev_y) / smoothening

            screen_x = np.interp(curr_x, [0, w], [0, screen_width])
            screen_y = np.interp(curr_y, [0, h], [0, screen_height])

            pyautogui.moveTo(screen_x, screen_y)

            prev_x, prev_y = curr_x, curr_y

        # Pinch (thumb + index) for left click
        dist_thumb_index = distance(norm_landmarks[4], norm_landmarks[8])
        if dist_thumb_index < 0.05:
            current_time = time.time()
            if current_time - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = current_time

        # Fist (all fingers down) for play/pause (spacebar)
        if fingers == [0, 0, 0, 0, 0]:
            pyautogui.press('space')
            time.sleep(0.5)  # avoid multiple presses

        # Two fingers up (index + middle) to scroll down
        if fingers == [0, 1, 1, 0, 0]:
            pyautogui.scroll(-20)
            time.sleep(0.3)

        # Thumb up for volume up
        if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
            pyautogui.press('volumeup')
            time.sleep(0.3)

        # Thumb down for volume down
        # Approximate by thumb tip below thumb base
        if norm_landmarks[4][1] > norm_landmarks[3][1] and all(f == 0 for f in fingers[1:]):
            pyautogui.press('volumedown')
            time.sleep(0.3)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
