# 🖐 Gesture Controlled PC using Webcam

Control your PC using hand gestures and a regular webcam. This project uses computer vision to detect and interpret hand gestures, mapping them to actions like moving the cursor, clicking, scrolling, adjusting volume, and more.

## ✨ Features

- 🖱 Cursor movement via hand tracking
- 👆 Left click with pinch gesture
- ✊ Media control (Pause/Play)
- 📜 Scrolling with finger count
- 🔊 Volume control with thumb gestures
- 🚀 Real-time using webcam (no special hardware needed)

## 🛠 Tech Stack

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## 📸 How It Works

1. Capture webcam feed using OpenCV.
2. Use MediaPipe to detect hand landmarks.
3. Analyze landmark positions to identify gestures.
4. Trigger system-level actions using PyAutoGUI.

## 🧪 Sample Gestures

| Gesture               | Action           |
| --------------------- | ---------------- |
| Open palm             | Move cursor      |
| Pinch (thumb + index) | Left click       |
| Fist                  | Play/Pause media |
| 2 Fingers Up          | Scroll down      |
| Thumb Up              | Volume up        |
| Thumb Down            | Volume down      |

## 📦 Installation

1. Clone this repo:

```bash
git clone https://github.com/yourusername/gesture-controlled-pc.git
cd gesture-controlled-pc
```
