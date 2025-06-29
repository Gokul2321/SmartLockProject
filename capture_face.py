import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture - Press S to Save", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('s'):
        cv2.imwrite("your_face.jpg", frame)
        print("✅ Face image saved as your_face.jpg")
        break
    elif key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

