import keyboard
from hand_gesture_recognizer import GestureRecognizer

# Dictionary to map gestures to keys
gesture_keys = {
    "fist": "down",
    "open_palm": "up",
    "three_fingers": "left",
    "two_fingers": "right",
}

# Track the current state of each gesture (active or not)
active_gestures = set()


def handle_gesture_state(gesture_name, state):
    """
    Handle the state of gestures and map to keyboard actions.
    :param gesture_name: Name of the gesture (e.g., 'fist', 'open_palm').
    :param state: State of the gesture ('appear', 'disappear').
    """
    key = gesture_keys.get(gesture_name)
    if not key:
        return

    if state == "appear" and gesture_name not in active_gestures:
        # Gesture appeared, press the key
        keyboard.press(key)
        active_gestures.add(gesture_name)
    elif state == "disappear" and gesture_name in active_gestures:
        # Gesture disappeared, release the key
        keyboard.release(key)
        active_gestures.remove(gesture_name)


# Gesture state handlers
def handle_fist(state):
    handle_gesture_state("fist", state)


def handle_open_palm(state):
    handle_gesture_state("open_palm", state)


def handle_three_fingers(state):
    handle_gesture_state("three_fingers", state)


def handle_two_fingers(state):
    handle_gesture_state("two_fingers", state)


# Initialize the recognizer
recognizer = GestureRecognizer()

# Register gestures and their handlers
recognizer.register_gesture("fist", handle_fist)
recognizer.register_gesture("open_palm", handle_open_palm)
recognizer.register_gesture("three_fingers", handle_three_fingers)
recognizer.register_gesture("two_fingers", handle_two_fingers)

# Run the recognizer
recognizer.run()
