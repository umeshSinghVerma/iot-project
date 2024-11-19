import keyboard
from hand_gesture_recognizer import GestureRecognizer
from hand_gesture_recognizer.custom_gestures import handle_four_fingers

# Dictionary to map gestures to keys
gesture_keys = {
    "fist": "down",
    "open_palm": "up",
    "three_fingers": "left",
    "two_fingers": "right"
}

# Track the current state of each gesture (active or not)
active_gestures = set()

def handle_gesture(gesture_name, is_active):
    key = gesture_keys[gesture_name]
    if is_active and gesture_name not in active_gestures:
        # Gesture detected and not already active, press the key
        keyboard.press(key)
        active_gestures.add(gesture_name)
    elif not is_active and gesture_name in active_gestures:
        # Gesture no longer detected but was active, release the key
        keyboard.release(key)
        active_gestures.remove(gesture_name)

def handle_cur_fist(image):
    handle_gesture("fist", True)

def handle_cur_open_palm(image):
    handle_gesture("open_palm", True)

def handle_cur_three_fingers(image):
    handle_gesture("three_fingers", True)

def handle_cur_two_fingers(image):
    handle_gesture("two_fingers", True)

def check_inactive_gestures(detected_gestures):
    # Release keys for gestures that are no longer active
    for gesture in list(active_gestures):
        if gesture not in detected_gestures:
            handle_gesture(gesture, False)

recognizer = GestureRecognizer()

# Register gestures
recognizer.register_gesture("fist", handle_cur_fist)
recognizer.register_gesture("open_palm", handle_cur_open_palm)
recognizer.register_gesture("four_fingers", handle_four_fingers)
recognizer.register_gesture("three_fingers", handle_cur_three_fingers)
recognizer.register_gesture("two_fingers", handle_cur_two_fingers)

# Modify recognizer loop to track inactive gestures
def run_recognizer():
    while True:
        detected_gestures = recognizer.get_active_gestures()  # Hypothetical method
        check_inactive_gestures(detected_gestures)
        recognizer.process_frame()  # Process next frame (method dependent on your recognizer)

run_recognizer()
