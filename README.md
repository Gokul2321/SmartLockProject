# 🔐 Smart Lock: Face + Gesture Authentication System

This project is a smart, software-based locking system built with **Python**, which uses **face recognition** and **hand gesture sequences** to unlock access. Perfect for securing files, folders, or custom systems.

---

## ✨ Features

- ✅ Face Recognition using **DeepFace**
- ✋ Gesture Detection using **MediaPipe**
- 🔐 Multi-step gesture password for extra security
- 🔒 Ready to integrate with file/folder encryption
- 🧠 Built using only software — no extra hardware required

---
 Run the Project
📸 1. Capture your face
```bash
python capture_face.py
```
✋ 2. Save your gesture sequence
```bash
python save_gestures.py
```
🔐 3. Run the smart lock
```bash
python smart_lock.py
```
🧠 Built With
DeepFace
MediaPipe
OpenCV
Python 3.10+

## 🛠 Requirements
opencv-python
deepface
mediapipe

## 🧩 File Structure

SmartLockProject/

├── capture_face.py         # Capture your face and save as your_face.jpg
├── save_gestures.py        # Save your custom gesture sequence
├── smart_lock.py           # Main lock script (face + gesture match)
├── your_face.jpg           # Your face image (not recommended to commit)
├── gesture_sequence.json   # Saved gesture password
├── requirements.txt        # Required packages
├── README.md               # Project documentation
└── .gitignore              # Files to exclude from Git

If you want it auto-generated from your actual environment, you can run:
```bash
 pip freeze > requirements.txt
 ```
Install dependencies using:

```bash
pip install -r requirements.txt
# SmartLockProject
