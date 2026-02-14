import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.8, tracking_confidence=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None
        
    def find_hands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        if draw and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
    
    def get_landmark_list(self, frame):
        h, w, _ = frame.shape
        lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def get_fingers_up(self, lm_list):
        if not lm_list:
            return [0, 0, 0, 0, 0]
            
        fingers = []
        if lm_list[4][1] < lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        tips = [8, 12, 16, 20]
        for tip in tips:
            if lm_list[tip][2] < lm_list[tip-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers