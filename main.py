'''
Welcome to (placeholder title)!
This is a rock paper scissors game based off a minigame from Brain Age for the Nintendo DS.
I grew up with a hand-me-down DS from my cousin and Brain Age was one of my favorite games.
I figured I'd try and recreate the rock paper scissors minigame but instead of saying rock
paper or scissors, the player will simply make the pose with their hand.
'''
#Import libraries
import cv2 as cv
import mediapipe as mp

#Declare and initialize variables
mpDrawing = mp.solutions.drawing_utils
mpDrawingStyles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands
handPose = "waiting for hand..."
gamePlay = False
gameText = ""

#Determine hand pose based on the position of landmarks (tracking points) on the hand
def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range (9, 20, 4)]): return "rock"
    elif all([landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks [20].y ]): return "scissors"
    else: return "paper"   

    

#Start video capture
vid = cv.VideoCapture(0)

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

        cv.putText(frame, f"Pose: {handPose}", (50,50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 1, cv.LINE_AA)
        cv.putText(frame, f'{gameText}', (50,100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)

        if gamePlay == False:
            gameText = 'Hold up "scissors" to begin!'
            cv.putText(frame, f'Press "q" to close.', (50,150), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
        
        if handPose == "scissors" and gamePlay == False:
            gamePlay = True

        if gamePlay == True:
            gameText = 'Game started!'

        cv.imshow('frame', frame)


        if cv.waitKey(1) & 0xFF == ord('q'): break
    
    vid.release()
    cv.destroyAllWindows()