import keyboard
from hand_gesture_recognizer import GestureRecognizer

# Dictionary to map gestures to keyboard or mouse actions
gesture_actions = {
    "fist": "down",
    "open_palm": "up",
    "two_fingers": "left",  # Click left mouse button
    "three_fingers": "right",  # Click right mouse button
}

# Track the current state of each gesture (active or not)
active_gestures = set()


def handle_gesture_state(gesture_name, state):
    """
    Handle the state of gestures and map to keyboard or mouse actions.
    :param gesture_name: Name of the gesture (e.g., 'fist', 'open_palm', 'two_fingers').
    :param state: State of the gesture ('appear', 'disappear').
    """
    action = gesture_actions.get(gesture_name)
    if not action:
        return

    if state == "appear" and gesture_name not in active_gestures:
        # Gesture appeared, perform the action
        if callable(action):
            action()  # Execute the action if it's a callable (e.g., mouse click)
        else:
            keyboard.press(action)
        active_gestures.add(gesture_name)
    elif state == "disappear" and gesture_name in active_gestures:
        # Gesture disappeared, release the key if it's a keyboard action
        if isinstance(action, str):  # Only release if it's a keyboard key
            keyboard.release(action)
        active_gestures.remove(gesture_name)


# Gesture state handlers
def handle_fist(state):
    handle_gesture_state("fist", state)


def handle_open_palm(state):
    handle_gesture_state("open_palm", state)


def handle_left_swipe(state):
    handle_gesture_state("two_fingers", state)


def handle_right_swipe(state):
    handle_gesture_state("three_fingers", state)


# Initialize the recognizer
recognizer = GestureRecognizer()

# Register gestures and their handlers
recognizer.register_gesture("fist", handle_fist)
recognizer.register_gesture("open_palm", handle_open_palm)
recognizer.register_gesture("two_fingers", handle_left_swipe)
recognizer.register_gesture("three_fingers", handle_right_swipe)

# Run the recognizer
recognizer.run()
