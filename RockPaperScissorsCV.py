import cv2 as cv
import mediapipe as mp

mpDrawing = mp.solutions.drawing_utils
mpDrawingStyles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands

handPose = "waiting for hand..."


def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range (9, 20, 4)]): return "rock"
    elif all([landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks [20].y ]): return "scissors"
    else: return "paper"

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

        cv.putText(frame, f"Pose: {handPose}", (50,50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)

        cv.imshow('frame', frame)


        if cv.waitKey(1) & 0xFF == ord('q'): break
    
    vid.release()
    cv.destroyAllWindows()