✊✋✌️ Rock Paper Scissors with hand Gestures.
A computer vision-based Rock, Paper, Scissors game built with Python 3.13 and OpenCV. This project uses Convexity Defects (mathematical geometry) to detect hand gestures, making it lightweight and compatible with the newest Python versions.

✨ Features

Real-Time Detection: Uses computer vision to recognize hand gestures via a webcam.

Interactive HUD: Features a transparent UI, live scoring, and victory overlays.

Countdown System: Arcade-style "3... 2... 1..." timer for fair play.

Lightweight: No heavy machine learning model required.

Debug Mode: Includes a threshold view to help calibrate lighting.

🛠️ Prerequisites
Python 3.13 (or any version 3.x)

A Webcam

📦 Installation
Clone or Download this repository.

Install the required libraries using pip:

Bash

pip install opencv-python numpy

🚀 How to Run

Save the game code as gesture_rps.py.

Run the script:

Bash

python game.py

Two windows will open:

Rock Paper Scissors UI: The main game screen.

Hand Calibration: A black and white view for debugging.

🎮 How to Play

Position your hand: Place your hand inside the Green Box on the screen.

Calibrate: Ensure your hand looks White and the background looks Black in the calibration window. (Use a plain background for best results).

Start Round: Press SPACEBAR to start the countdown.

Make your Move: Hold your gesture (Rock, Paper, or Scissors) until the countdown hits 0.

✊ Rock: Fist (0 fingers extended).

✌️ Scissors: "V" sign (Index and Middle finger extended).

✋ Paper: All fingers extended.

Replay: Press SPACEBAR to play again.

Quit: Press Q to exit.

🔧 Troubleshooting
Camera Not Detected / Error: Index out of range
If you are using a laptop (especially MSI), try these steps:

Check Keyboard Lock: Press Fn + F6 (or just F6) to ensure your webcam is enabled.

Change Index: Open the code and change the camera index line:

Python

# Change 0 to 1
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
Jumpy / Inaccurate Detection
Since this version relies on color thresholding.

Lighting: Ensure the room is well-lit.

Background: Use a plain wall behind your hand.

Shadows: Avoid strong shadows inside the green box.

🧠 How it Works (The Math)
Instead of AI, this program uses Convexity Defects:

It finds the Contour (outline) of your hand.

It creates a Convex Hull (a tight envelope around the hand).

It calculates the Defects (the deep gaps between fingers).

0 Gaps: Rock

1 Deep Gap: Scissors

2 Gaps: Paper


Authors: Praveen Thanvi (233501167), Khush Purohit (233501093) and Yuvraj Suthar (233501236)
Built with: Python & OpenCV
