import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self, maxHands=1):
        self.hands = mp.solutions.hands.Hands(max_num_hands=maxHands)
        self.drawer = mp.solutions.drawing_utils

    def get_landmarks(self, image):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)
        landmarks = []

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                for lm in hand.landmark:
                    landmarks.append((lm.x, lm.y))
                self.drawer.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)

        return landmarks
