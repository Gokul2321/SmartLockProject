import cv2
from deepface import DeepFace
import mediapipe as mp
import json
import os

# --- Load gesture sequence ---
with open("gesture_sequence.json", "r") as f:
    gesture_sequence = json.load(f)

gesture_step = 0
gesture_verified = False
gesture_timeout = 100

# --- Setup MediaPipe for hands ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# --- Helper Function to Check Which Fingers Are Up ---
def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = []
    fingers.append(lm[4].x < lm[3].x)        # Thumb
    fingers.append(lm[8].y < lm[6].y)        # Index
    fingers.append(lm[12].y < lm[10].y)      # Middle
    fingers.append(lm[16].y < lm[14].y)      # Ring
    fingers.append(lm[20].y < lm[18].y)      # Pinky
    return fingers

# --- Load your registered face image ---
registered_face = "your_face.jpg"

# --- Start webcam ---
cap = cv2.VideoCapture(0)
face_verified = False
gesture_verified = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # --- FACE VERIFICATION ---
    if not face_verified:
        if os.path.exists(registered_face):
            try:
                face_result = DeepFace.verify(frame, registered_face, enforce_detection=False)
                if face_result["verified"]:
                    face_verified = True
                    print("✅ Face Match: Accessing Gesture Lock")
            except Exception as e:
                print("❌ Face verification error:", e)
        else:
            print("❌ your_face.jpg not found!")

    # --- GESTURE VERIFICATION ---
    if face_verified and not gesture_verified:
        results = hands.process(rgb)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                current = fingers_up(handLms)

                expected = gesture_sequence[gesture_step]
                if current == expected:
                    gesture_step += 1
                    print(f"✅ Step {gesture_step} correct!")
                    if gesture_step == len(gesture_sequence):
                        gesture_verified = True
                        print("✅ Full gesture sequence matched!")
                        break
                else:
                    gesture_timeout -= 1
                    if gesture_timeout <= 0:
                        gesture_step = 0
                        gesture_timeout = 100
                        print("❌ Sequence reset due to timeout or mismatch")

    # --- Display UI Text ---
    if not face_verified:
        cv2.putText(frame, "Scan Face...", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    elif face_verified and not gesture_verified:
        cv2.putText(frame, "Face Verified ✅ - Show Gesture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    elif face_verified and gesture_verified:
        cv2.putText(frame, "UNLOCKED 🔓✅", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Smart Lock 🔐", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



