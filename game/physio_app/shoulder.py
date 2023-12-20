import cv2
import mediapipe as mp
import math
import pyttsx3

def run_game():
    engine = pyttsx3.init()
    def calculate_angle(a, b, c):
        angle_rad = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        angle_deg = abs(math.degrees(angle_rad))
        return angle_deg
    def calculate_accuracy(angle, optimal_angle=90):
        proximity = 1 - abs((angle - optimal_angle) / optimal_angle)
        accuracy = max(0, min(100, proximity * 100))
        return accuracy
    def check_exercise1(posture_landmarks):
        # Right
        right_waist = (posture_landmarks[24][0], posture_landmarks[24][1])
        right_shoulder = (posture_landmarks[12][0], posture_landmarks[12][1])
        right_hand = (posture_landmarks[16][0], posture_landmarks[16][1])
        right_angle = calculate_angle(right_waist, right_shoulder, right_hand)
        # Left
        left_waist = (posture_landmarks[23][0], posture_landmarks[23][1])
        left_shoulder = (posture_landmarks[11][0], posture_landmarks[11][1])
        left_hand = (posture_landmarks[15][0], posture_landmarks[15][1])
        left_angle = calculate_angle(left_waist, left_shoulder, left_hand)

        optimal_angle = 90

        if left_angle > optimal_angle and right_angle > optimal_angle:
            return True, (left_angle, right_angle)
        else:
            return False, (left_angle, right_angle)

    def main():
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)
        count_exercise1 = 0
        correct_display_time = 0  
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(img)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in
                                results.pose_landmarks.landmark]
                    correct, angles = check_exercise1(landmarks)
                    if correct:
                        count_exercise1 += 1
                        left_accuracy = calculate_accuracy(angles[0])
                        right_accuracy = calculate_accuracy(angles[1])
                        average_accuracy = (left_accuracy + right_accuracy) / 2
                        engine.say(f"Correct {count_exercise1}.")
                        engine.runAndWait()
                        cv2.putText(frame, f'Correct ({count_exercise1})  Accuracy {average_accuracy:.2f}%', (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                        correct_display_time = 50 
                    elif correct_display_time > 0:
                        cv2.putText(frame, f'Correct ({count_exercise1})  Accuracy {average_accuracy:.2f}%', (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                        correct_display_time -= 1

                    else:
                        cv2.putText(frame, 'Exercise 1: Incorrect', (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow('Posture Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    if __name__ == "__main__":
        main()
