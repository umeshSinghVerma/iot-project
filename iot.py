import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands and Drawing utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# Custom functions for each gesture
def handle_fist(image):
    cv2.putText(
        image,
        "Fist",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_open_palm(image):
    cv2.putText(
        image,
        "Open Palm",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_two_fingers(image):
    cv2.putText(
        image,
        "Two Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_three_fingers(image):
    cv2.putText(
        image,
        "Three Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_four_fingers(image):
    cv2.putText(
        image,
        "Four Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


# Function to detect gestures
def detect_gesture(hand_landmarks):
    # Check if fingers are extended using their TIP and PIP landmarks
    fingers_extended = []

    # Thumb (compare X coordinate since it's oriented differently)
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    fingers_extended.append(thumb_tip.x < thumb_ip.x)  # Left hand; reverse for right

    # Other fingers (compare TIP and PIP landmarks)
    for finger_tip, finger_pip in [
        (
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.INDEX_FINGER_PIP,
        ),
        (
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        ),
        (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
    ]:
        tip = hand_landmarks.landmark[finger_tip]
        pip = hand_landmarks.landmark[finger_pip]
        fingers_extended.append(tip.y < pip.y)

    # Count extended fingers
    extended_count = sum(fingers_extended)

    if extended_count == 0:
        return "fist"
    elif extended_count == 5:
        return "open_palm"
    elif extended_count == 4:
        return "four_fingers"
    elif extended_count == 3:
        return "three_fingers"
    elif extended_count == 2:
        return "two_fingers"
    return None


# Open the webcam
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Process the image
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        # Convert the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Create a blank mask for the hand
        hand_mask = np.zeros_like(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Detect gesture
                gesture = detect_gesture(hand_landmarks)

                # Call the corresponding function
                if gesture == "fist":
                    handle_fist(image)
                elif gesture == "open_palm":
                    handle_open_palm(image)
                elif gesture == "two_fingers":
                    handle_two_fingers(image)
                elif gesture == "three_fingers":
                    handle_three_fingers(image)
                elif gesture == "four_fingers":
                    handle_four_fingers(image)

                # Draw the landmarks and create a hand mask
                mp_drawing.draw_landmarks(
                    hand_mask,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2, circle_radius=2
                    ),
                    mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2, circle_radius=2
                    ),
                )

        # Create a grayscale version of the mask
        gray_hand_mask = cv2.cvtColor(hand_mask, cv2.COLOR_BGR2GRAY)
        _, binary_hand_mask = cv2.threshold(gray_hand_mask, 10, 255, cv2.THRESH_BINARY)

        # Show the original image and hand mask side by side
        combined_view = np.hstack(
            (image, cv2.cvtColor(binary_hand_mask, cv2.COLOR_GRAY2BGR))
        )
        cv2.imshow("Hand Gesture Recognition and Mask", combined_view)

        # Exit on pressing 'ESC'
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
