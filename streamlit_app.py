import cv2
import mediapipe as mp
import math
import winsound
import threading
import streamlit as st

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_holistic = mp.solutions.holistic

# Initialize the holistic detector
holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Flag to track if a thread is already running
sound_thread_running = False

def play_alert_sound():
    global sound_thread_running
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    sound_thread_running = False

def app():
    global sound_thread_running
    st.title("Real Time Distracted Driver Detection")

    col,col2,col3 = st.columns([1,3,1])
    stframe = st.empty()
    start_button = col.button("Start")
    end_button = col3.button("End")

    if start_button and not end_button:
            cap = cv2.VideoCapture(0)  # Open the default camera
            alert_message = ""

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    st.warning("Ignoring empty camera frame.")
                    continue

                # Convert the image to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Perform holistic detection
                results = holistic.process(image)

                # Convert the image back to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Draw the face mesh, body, and hand annotations on the image
                mp_drawing.draw_landmarks(
                    image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                )

                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                mp_drawing.draw_landmarks(
                    image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                mp_drawing.draw_landmarks(
                    image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                # Check if any hand landmark is within a certain distance from the face landmark
                alert_message = ""
                play_sound = False
                if results.face_landmarks and (results.left_hand_landmarks or results.right_hand_landmarks):
                    face_x, face_y = results.face_landmarks.landmark[4].x, results.face_landmarks.landmark[4].y

                    if results.left_hand_landmarks:
                        hand_x, hand_y = results.left_hand_landmarks.landmark[9].x, results.left_hand_landmarks.landmark[9].y
                        distance = math.sqrt((face_x - hand_x) ** 2 + (face_y - hand_y) ** 2)
                        if distance < 0.19:
                            alert_message = "Alert! Driver is using mobile."
                            play_sound = True

                    if results.right_hand_landmarks:
                        hand_x, hand_y = results.right_hand_landmarks.landmark[9].x, results.right_hand_landmarks.landmark[9].y
                        distance = math.sqrt((face_x - hand_x) ** 2 + (face_y - hand_y) ** 2)
                        if distance < 0.19:
                            alert_message = "Alert! Driver is using mobile."
                            play_sound = True

                # Play the alert sound in a separate thread if the condition is met and no thread is already running
                if play_sound and not sound_thread_running:
                    if sound_thread_running:
                        # Kill the existing thread if it's still running
                        sound_thread.join()
                    sound_thread = threading.Thread(target=play_alert_sound)
                    sound_thread.start()
                    sound_thread_running = True

                # Print the alert message on the screen
                cv2.putText(image, alert_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Display the image in Streamlit
                stframe.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB")

            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    app()