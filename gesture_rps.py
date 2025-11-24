import cv2
import numpy as np
import random
import time

#CONFIGURATIONS
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

# Game Variables
scores = {"Player": 0, "CPU": 0}
state = "WAITING" # States: WAITING, COUNTDOWN, RESULT
timer_start = 0
player_move = "None"
cpu_move = "?"
result_text = ""
color_dict = {"Rock": (255, 0, 0), "Paper": (0, 255, 0), "Scissors": (0, 0, 255)} # BGR

def draw_ui(img, p_move, c_move, res, p_score, c_score, state, timer):
    h, w, _ = img.shape
    
    # 1. Create a semi-transparent sidebar for CPU
    overlay = img.copy()
    cv2.rectangle(overlay, (w-250, 0), (w, h), (30, 30, 30), -1) # Dark sidebar
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)       # Top bar
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # 2. Draw ROI Box (Where you put your hand)
    cv2.rectangle(img, (50, 100), (250, 300), (0, 255, 0), 2)
    cv2.putText(img, "PLACE HAND HERE", (55, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 3. Scores
    cv2.putText(img, f"YOU: {p_score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f"CPU: {c_score}", (w-230, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 4. CPU Move Display (Big Box on Right)
    cv2.rectangle(img, (w-220, 150), (w-30, 340), (255, 255, 255), 2)
    
    if state == "RESULT":
        # Draw CPU Text
        color = color_dict.get(c_move, (255, 255, 255))
        cv2.putText(img, c_move, (w-210, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        
        # Draw Result Text (Big Center Overlay)
        res_color = (0, 255, 0) if "Win" in res else (0, 0, 255) if "CPU" in res else (0, 255, 255)
        cv2.putText(img, res, (w//2 - 150, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, res_color, 4)
        cv2.putText(img, "Press SPACE to Replay", (w//2 - 120, h//2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    elif state == "COUNTDOWN":
        remaining = 3 - int(time.time() - timer)
        cv2.putText(img, str(remaining), (w//2 - 20, h//2), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 255), 5)
    
    else: # WAITING
        cv2.putText(img, "CPU READY", (w-210, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)
        cv2.putText(img, "Press SPACE to Start", (w//2 - 150, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return img

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    
    #HAND DETECTION LOGIC (The "Green Box" Engine)
    roi = frame[100:300, 50:250] # Adjusted coordinates for layout
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    current_gesture = "Unknown"
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(cnt, returnPoints=False)
        if hull.shape[0] > 3:
            defects = cv2.convexityDefects(cnt, hull)
            fingers = 0
            if defects is not None:
                for i in range(defects.shape[0]):
                    if defects[i, 0][3] > 10000: fingers += 1
            current_gesture = "Rock" if fingers == 0 else "Scissors" if fingers == 1 else "Paper"

    #GAME STATE MACHINE
    key = cv2.waitKey(1)
    
    if state == "WAITING":
        if key == 32: # Spacebar
            state = "COUNTDOWN"
            timer_start = time.time()
            
    elif state == "COUNTDOWN":
        # Check if 3 seconds passed
        if time.time() - timer_start > 3:
            cpu_move = random.choice(["Rock", "Paper", "Scissors"])
            player_move = current_gesture
            
            # Win Check
            if player_move == cpu_move:
                result_text = "DRAW"
            elif (player_move == "Rock" and cpu_move == "Scissors") or \
                 (player_move == "Scissors" and cpu_move == "Paper") or \
                 (player_move == "Paper" and cpu_move == "Rock"):
                result_text = "YOU WIN!"
                scores["Player"] += 1
            else:
                result_text = "CPU WINS!"
                scores["CPU"] += 1
            
            state = "RESULT"

    elif state == "RESULT":
        if key == 32: # Spacebar to restart
            state = "WAITING"
            player_move = "None"
            cpu_move = "?"

    # Draw everything
    frame = draw_ui(frame, player_move, cpu_move, result_text, scores["Player"], scores["CPU"], state, timer_start)
    
    # Show debug window for hand calibration
    cv2.imshow("Hand Calibration (Make this Black/White)", thresh)
    cv2.imshow("Rock Paper Scissors UI", frame)
    
    if key == ord('q'): break

cap.release()
cv2.destroyAllWindows()