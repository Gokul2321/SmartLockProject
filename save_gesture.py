import cv2
import mediapipe as mp
import json

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = []
    fingers.append(lm[4].x < lm[3].x)  # Thumb
    fingers.append(lm[8].y < lm[6].y)  # Index
    fingers.append(lm[12].y < lm[10].y)  # Middle
    fingers.append(lm[16].y < lm[14].y)  # Ring
    fingers.append(lm[20].y < lm[18].y)  # Pinky
    return fingers

cap = cv2.VideoCapture(0)
saved = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            current = fingers_up(handLms)

            # Show live finger status
            cv2.putText(frame, f"Gesture: {current}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                with open("gesture_password.json", "w") as f:
                    json.dump(current, f)
                print("✅ Gesture saved as gesture_password.json:", current)
                saved = True
                break

    cv2.imshow("Show Gesture - Press S to Save", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or saved:
        break

cap.release()
cv2.destroyAllWindows()

