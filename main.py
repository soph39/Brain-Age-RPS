'''
Welcome to RPS Speed Trial!
This is a rock paper scissors game inspired by a minigame from Brain Age for the Nintendo DS.
I grew up with a hand-me-down DS from my cousin and Brain Age was one of my favorite games.
I figured I'd try and recreate the rock paper scissors minigame but instead of saying rock
paper or scissors, the player will simply make the pose with their hand.

Version: 0.1.0

Note for dev (she is forgetful):
Use pyinstaller --noconfirm --collect-submodules=mediapipe --collect-data=mediapipe main.py to compile
'''
#Import libraries
import cv2 as cv
import mediapipe as mp
import threading
import random
import time

#Declare and initialize variables
mpDrawing = mp.solutions.drawing_utils
mpDrawingStyles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands
handPose = "waiting for hand..."
gamePlay = False
gameText = ""
gameText2 = ""
gameFinish = False
timeStore = 0.0
cameraOption = 0

#Start video capture
vid = cv.VideoCapture(cameraOption)

#Determine hand pose based on the position of landmarks (tracking points) on the hand
def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range (9, 20, 4)]): return "rock"
    elif all([landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks [20].y ]): return "scissors"
    else: return "paper"   

def playGame():
    global gameText, gamePlay, gameText2
    choiceList = ["rock", "paper", "scissors"]
    conditionList = ["win", "lose", "tie"]
    oppChoice = ""
    condition = ""
    win = False
    score = 0
    scoreStore = 0
    gamePlay = True

    gameText = 'Game started!'
    threading.Event().wait(2)
    for i in range(5):
        oppChoice = random.choice(choiceList)
        condition = random.choice(conditionList)
        for j in range(1, 4):
            gameText = f"{j}..."
            threading.Event().wait(1)
        gameText = f'{oppChoice.capitalize()} | {condition.capitalize()}'
        win = False
        gameText2 = "Waiting..."
        timeStore = time.time()
        while win == False:
            time.sleep(0.001)
            match condition:
                case "win":
                    match handPose:
                        case "rock":
                            if oppChoice == "scissors":
                                win = True
                            else:  
                                win = False

                        case "paper":
                            if oppChoice == "rock":
                                win = True
                            else:
                                win = False

                        case "scissors":
                            if oppChoice == "paper":
                                win = True
                            else:
                                win = False

            
                case "lose":
                    match handPose:
                        case "rock":
                            if oppChoice == "paper":
                                win = True
                            else:
                                win = False

                        case "paper":
                            if oppChoice == "scissors":
                                win = True
                            else:
                                win = False

                        case "scissors":
                            if oppChoice == "rock":
                                win = True
                            else:
                                win = False
            
                case "tie":
                    if oppChoice == handPose:
                        win = True
                    else:
                        win = False
        else:
            scoreStore = float(time.time()) - float(timeStore)
            score += scoreStore
            gameText2 = "Correct! Seconds: " + str("%.4f" % round(scoreStore, 4))
            gameStart = False
        threading.Event().wait(1)
        i+=1
    
    gameText = "Done! Total seconds: " + str("%.4f" % round(score, 4))
    gameText2 = 'Press "q" to close.'

with mpHands.Hands(model_complexity=0,
                   min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = vid.read()
        if not ret or frame is None: break
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        results = hands.process(frame)

        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpDrawing.draw_landmarks(frame,
                                         hand_landmarks,
                                          mpHands.HAND_CONNECTIONS,
                                          mpDrawingStyles.get_default_hand_landmarks_style(),
                                          mpDrawingStyles.get_default_hand_connections_style())
                
        frame = cv.flip(frame,1)

        handResult = results.multi_hand_landmarks
        if handResult and len(handResult) != 0 :
            handPose = getHandMove(handResult[0])
        else: handPose = "Waiting for hand..."

        cv.putText(frame, f"Pose: {handPose.capitalize()}", (50,50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 1, cv.LINE_AA)
        cv.putText(frame, f'{gameText}', (50,100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, f'{gameText2}', (50,150), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)

        if not gamePlay:
            gameText = 'Hold up "scissors" to begin!'
            cv.putText(frame, f'Press SPACE to change camera.', (50,200), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
            cv.putText(frame, f'Press "q" to close.', (50,150), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
        
        if handPose == "scissors" and not gamePlay:
            threading.Thread(target=playGame, daemon=True).start()
        
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'): break

    
    vid.release()
    cv.destroyAllWindows()