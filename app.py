import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# Set page layout and title
st.set_page_config(page_title="Gesture Control PC", layout="wide")
st.title("🖐️ Gesture-Controlled PC Interface")
st.markdown("""
Control your computer with hand gestures using your webcam!  
**Gestures:**  
- Open palm: Move cursor  
- Pinch (thumb+index): Left click  
- Fist: Play/Pause  
- Two fingers: Scroll down  
- Thumb up/down: Volume up/down  
""")

# Webcam video placeholder
video_placeholder = st.empty()
status_text = st.empty()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0
smoothening = 7
click_delay = 0.3
last_click_time = 0

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

while True:
    success, img = cap.read()
    if not success:
        status_text.text("⚠️ Cannot access webcam")
        break

    img = cv2.flip(img, 1)  # Mirror image so it feels natural

    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    status = "No hand detected"

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append((int(lm.x * w), int(lm.y * h)))
        norm_landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

        fingers = fingers_up(norm_landmarks)

        # Gesture detection & action

        if fingers == [1,1,1,1,1]:
            status = "Moving cursor"
            x, y = landmarks[8]
            curr_x = prev_x + (x - prev_x) / smoothening
            curr_y = prev_y + (y - prev_y) / smoothening
            screen_x = np.interp(curr_x, [0,w], [0,screen_width])
            screen_y = np.interp(curr_y, [0,h], [0,screen_height])
            pyautogui.moveTo(screen_x, screen_y)
            prev_x, prev_y = curr_x, curr_y

        dist_thumb_index = distance(norm_landmarks[4], norm_landmarks[8])
        if dist_thumb_index < 0.05:
            current_time = time.time()
            if current_time - last_click_time > click_delay:
                status = "Click!"
                pyautogui.click()
                last_click_time = current_time

        if fingers == [0,0,0,0,0]:
            status = "Play/Pause"
            pyautogui.press('space')
            time.sleep(0.5)

        if fingers == [0,1,1,0,0]:
            status = "Scrolling down"
            pyautogui.scroll(-20)
            time.sleep(0.3)

        if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
            status = "Volume Up"
            pyautogui.press('volumeup')
            time.sleep(0.3)

        if norm_landmarks[4][1] > norm_landmarks[3][1] and all(f == 0 for f in fingers[1:]):
            status = "Volume Down"
            pyautogui.press('volumedown')
            time.sleep(0.3)

    status_text.text(f"Status: {status}")

    # Convert BGR image to RGB and display in Streamlit
    video_placeholder.image(img, channels="BGR", use_column_width=True)

cap.release()
