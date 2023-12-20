import cv2
import mediapipe as mp
import math
import pyttsx3
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
def main(age=30,injury=False):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    count_exercise1 = 0
    correct_display_time = 0  
    prev_state=None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            sucess,frame=cap.read()
            if not sucess:
                break
            else:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(img)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in
                                results.pose_landmarks.landmark]
                right_waist = (landmarks[24][0],landmarks[24][1])
                right_shoulder = (landmarks[12][0], landmarks[12][1])
                right_hand = (landmarks[16][0], landmarks[16][1])
                angle_rad = math.atan2(right_hand[1] - right_shoulder[1], right_hand[0] - right_shoulder[0]) - math.atan2(right_waist[1] - right_shoulder[1], right_waist[0] - right_shoulder[0])
                right_angle = abs(math.degrees(angle_rad))
                # Left
                left_waist = (landmarks[23][0], landmarks[23][1])
                left_shoulder = (landmarks[11][0], landmarks[11][1])
                left_hand = (landmarks[15][0], landmarks[15][1])
                angle_rad = math.atan2(left_hand[1] - left_shoulder[1], left_hand[0] - left_shoulder[0]) - math.atan2(left_waist[1] - left_shoulder[1], left_waist[0] - left_shoulder[0])
                left_angle = abs(math.degrees(angle_rad))
                # age
                optimal_angle=90
                if injury or age>55:
                    correct_angle_range = (70, 100)
                else:
                    correct_angle_range = (85, 95)
                
                if correct_angle_range[0] < right_angle < correct_angle_range[1] and correct_angle_range[0] < left_angle < correct_angle_range[1]:
                    correct=True
                    angles=(left_angle, right_angle)
                else:
                    correct=False
                    angles=(left_angle, right_angle)
                
                if correct:
                    if prev_state!='correct':
                        count_exercise1 += 1
                    proximity = 1 - abs((angles[0] - optimal_angle) / optimal_angle)
                    left_accuracy = max(0, min(100, proximity * 100))
                    
                    proximity = 1 - abs((angles[1] - optimal_angle) / optimal_angle)
                    right_accuracy = max(0, min(100, proximity * 100))
                    average_accuracy = (left_accuracy + right_accuracy) / 2
                    # engine.say(f"Correct {count_exercise1}.")
                    # engine.runAndWait()
                    cv2.putText(frame, f'Correct ({count_exercise1})  Accuracy {average_accuracy:.2f}%', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    prev_state='correct'
                    correct_display_time = 30 
                elif correct_display_time > 0:
                    cv2.putText(frame, f'Correct ({count_exercise1})  Accuracy {average_accuracy:.2f}%', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    prev_state='correct'
                    
                    correct_display_time -= 1

                else:
                    cv2.putText(frame, 'Exercise 1: Incorrect', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    prev_state='incorrect'
                    
                    
                ret,buffer= cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

   

if __name__ == "__main__":
    main()
