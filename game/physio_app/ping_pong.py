import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import csv

def run_game():

    file = open('ping_pong.xlsx', 'r')
    file =  csv.writer(file)
   
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Importing all images
    imgBackground = cv2.imread("physio_app//static//assets//img\Games//Background.png")
    imgGameOver = cv2.imread("physio_app//static//assets//img\Games//gameOver.png")
    imgBall = cv2.imread("physio_app//static//assets//img\Games//Ball.png", cv2.IMREAD_UNCHANGED)
    imgBat1 = cv2.imread("physio_app//static//assets//img\Games//bat1.png", cv2.IMREAD_UNCHANGED)
    imgBat2 = cv2.imread("physio_app//static//assets//img\Games//bat2.png", cv2.IMREAD_UNCHANGED)

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Variables
    ballPos = [100, 100]
    speedX = 15
    speedY = 15
    gameOver = False
    score = [0, 0]
    level = 1
    incorrect_gesture_timer = 0
    correct_gesture_timer = 0
    hand_alert_timer = 0

    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgRaw = img.copy()

        # Find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw

        # Overlaying the background image
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        # Display "Alert!!!" when no hand is detected
        if not hands:
            cv2.putText(img, "Alert !!!", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            hand_alert_timer = time.time()
        else:
            # Check for hands
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1
                        correct_gesture_timer = time.time()
                        incorrect_gesture_timer = 0  # Reset the timer for incorrect gesture
                    else:
                        incorrect_gesture_timer = time.time()

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] -= 30
                        score[1] += 1
                        correct_gesture_timer = time.time()
                        incorrect_gesture_timer = 0  # Reset the timer for incorrect gesture
                    else:
                        incorrect_gesture_timer = time.time()

        # Game Over
        if ballPos[0] < 40 or ballPos[0] > 1200:
            if level == 1 and score[1] + score[0] < 5:
                gameOver = True
            else:
                gameOver = True

        if gameOver:
            img = imgGameOver
            if level == 1 and score[1] + score[0] < 5:
                cv2.putText(img, "Game Over!", (50, 360),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 200), 3)
                cv2.putText(img, "Press 'R' to Play Again", (250, 450),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 200), 3)
            else:
                cv2.putText(img, f"Total Score: {score[1] + score[0]} | Level: {level}", (250, 360),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 200), 3)
                cv2.putText(img, "Press 'R' to Play Again", (250, 450),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 200), 3)

            # Check for 'R' key press to restart the game
            key = cv2.waitKey(1)
            if key == ord('r'):
                ballPos = [100, 100]
                speedX = 15
                speedY = 15
                gameOver = False
                score = [0, 0]
                level = 1
                imgGameOver = cv2.imread("Resources/gameOver.png")
                correct_gesture_timer = 0
                incorrect_gesture_timer = 0
                hand_alert_timer = 0
        else:
            # If game not over move the ball
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            # Draw the ball
            img = cvzone.overlayPNG(img, imgBall, ballPos)

            # Display level
            cv2.putText(img, f"Level: {level}", (550, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

            cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

            # Increase level and speed
            if score[1] + score[0] >= level * 5:
                level += 1
                speedX += 5
                speedY += 5

            # Display "Correct Gestures!" for 2 seconds after detecting a correct gesture
            if time.time() - correct_gesture_timer < 2:
                cv2.putText(img, "Correct Gestures!", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                # Wipe out "Incorrect Gestures!"
                cv2.putText(img, "", (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

            # Display "Incorrect Gestures!" for 0.2 seconds after detecting an incorrect gesture
            # if time.time() - incorrect_gesture_timer < 0.2:
            #     cv2.putText(img, "Incorrect Gestures!", (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

        # Display "Alert!!!" for 2 seconds after no hand is detected
        if time.time() - hand_alert_timer < 2:
            cv2.putText(img, "Alert!!!", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

        img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            ballPos = [100, 100]
            speedX = 15
            speedY = 15
            gameOver = False
            score = [0, 0]
            level = 1
            imgGameOver = cv2.imread("Resources/gameOver.png")
            correct_gesture_timer = 0
            incorrect_gesture_timer = 0
            hand_alert_timer = 0
