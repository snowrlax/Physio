import cv2
import mediapipe as mp
import math
import pyttsx3

engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
def main(age=38,injury=False):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    count_leg_exercise = 0
    correct_display_time = 0  # Time to display "Correct" in milliseconds
    prev_state=None
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            sucess, frame = cap.read()
            if not sucess:
                break
            else:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(img)
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    posture_landmarks = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in results.pose_landmarks.landmark]
                right_hip = (posture_landmarks[23][0], posture_landmarks[23][1])
                right_knee = (posture_landmarks[25][0], posture_landmarks[25][1])
                right_ankle = (posture_landmarks[27][0], posture_landmarks[27][1])
                angle_rad = math.atan2(right_ankle[1] - right_knee[1], right_ankle[0] - right_knee[0]) - math.atan2(right_hip[1] - right_knee[1], right_hip[0] - right_knee[0])
                right_angle = abs(math.degrees(angle_rad))
                
                # Left leg
                left_hip = (posture_landmarks[24][0], posture_landmarks[24][1])
                left_knee = (posture_landmarks[26][0], posture_landmarks[26][1])
                left_ankle = (posture_landmarks[28][0], posture_landmarks[28][1])
                angle_rad = math.atan2(left_ankle[1] - left_knee[1], left_ankle[0] - left_knee[0]) - math.atan2(left_hip[1] - left_knee[1], left_hip[0] - left_knee[0])
                left_angle = abs(math.degrees(angle_rad))
                # Define angle range for correct leg exercise
                if injury or age>55:
                    correct_angle_range = (70, 100)
                else:
                    correct_angle_range = (80, 95)
                optimal_angle=90
                if correct_angle_range[0] < right_angle < correct_angle_range[1] or \
                correct_angle_range[0] < left_angle < correct_angle_range[1]:
                    correct= True
                    angles=(right_angle, left_angle)
                else:
                    correct= False
                    angles=(right_angle, left_angle)
                if correct:
                    if prev_state!='correct':
                        count_leg_exercise += 1
                    proximity = 1 - abs((angles[0] - optimal_angle) / optimal_angle)
                    left_accuracy = max(0, min(100, proximity * 100))
                    
                    proximity = 1 - abs((angles[1] - optimal_angle) / optimal_angle)
                    right_accuracy = max(0, min(100, proximity * 100))
                    average_accuracy = (right_accuracy + left_accuracy)
                    cv2.putText(frame, f'Correct ({count_leg_exercise}) Accuracy {average_accuracy:.2f}%', (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    
                    prev_state='correct'

                    correct_display_time = 30  

                elif correct_display_time > 0:
                    cv2.putText(frame, f'Correct ({count_leg_exercise}) Accuracy {average_accuracy:.2f}%', (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    prev_state='correct'
                    
                    correct_display_time -= 1

                else:
                    cv2.putText(frame, 'Incorrect', (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    prev_state='incorrect'
                    
                ret,buffer= cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == "__main__":
    main()
