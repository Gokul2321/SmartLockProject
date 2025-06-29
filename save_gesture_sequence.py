import cv2
import mediapipe as mp
import json

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    return [
        lm[4].x < lm[3].x,      # Thumb
        lm[8].y < lm[6].y,      # Index
        lm[12].y < lm[10].y,    # Middle
        lm[16].y < lm[14].y,    # Ring
        lm[20].y < lm[18].y     # Pinky
    ]

cap = cv2.VideoCapture(0)
sequence = []

print("📸 Show each gesture, press 's' to save, 'q' to finish")

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
            cv2.putText(frame, f"Detected: {current}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Save Gesture Sequence", frame)
    key = cv2.waitKey(1)

    if key & 0xFF == ord('s'):
        if results.multi_hand_landmarks:
            sequence.append(current)
            print(f"✅ Saved gesture {len(sequence)}: {current}")
    elif key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save sequence
with open("gesture_sequence.json", "w") as f:
    json.dump(sequence, f)
print("📁 Saved sequence to gesture_sequence.json")

