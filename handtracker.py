import cv2
import mediapipe as mp
import mediapipe.python.solutions.drawing_styles as drawing_styles

mp_hands = mp.solutions.hands
hand = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


def is_thumb_up(results, img):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            thumb_left_up = thumb_is_up_left(hand_landmarks)
            thumb_right_up = thumb_is_up_right(hand_landmarks)
            hand_open_left = hand_open_thumb_left(hand_landmarks)
            hand_open_right = hand_open_thumb_right(hand_landmarks)

            if thumb_left_up and not hand_open_left:
                print("thumb left")
                return True
            if thumb_right_up and not hand_open_right:
                print("thumb right")
                return True
            if only_thumb_up(hand_landmarks):
                print("only thumb")
                return True

        return False


def thumb_is_up_right(hand_landmarks):
    return (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_DIP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x > hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x > hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_DIP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x > hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_DIP].x and only_thumb_up(hand_landmarks))


def thumb_is_up_left(hand_landmarks):
    return (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_MCP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_MCP].x and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_MCP].x and only_thumb_up(hand_landmarks))


def hand_open_thumb_left(hand_landmarks):
    return (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x < hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_DIP].x or
            hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x or hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_PIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_DIP].x or
            hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_DIP].x)


def hand_open_thumb_right(hand_landmarks):
    if (thumb_is_up_right(hand_landmarks) and
            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_PIP].x or
             hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x < hand_landmarks.landmark[
                 mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x or
             hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x < hand_landmarks.landmark[
                 mp_hands.HandLandmark.RING_FINGER_PIP].x or
             hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x < hand_landmarks.landmark[
                 mp_hands.HandLandmark.PINKY_PIP].x)):
        return True
    return False


def only_thumb_up(hand_landmarks):
    diff = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y - hand_landmarks.landmark[
        mp_hands.HandLandmark.THUMB_TIP].y
    if diff < 0.07:
        return False
    return (
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_TIP].y and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_MCP].y
            and hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y > hand_landmarks.landmark[
                mp_hands.HandLandmark.THUMB_TIP].y)


def is_thumb_down_left(hand_landmarks):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.PINKY_PIP
    ]

    thumb_down_left = True
    for finger in fingers_idx:
        if hand_landmarks.landmark[finger].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
            thumb_down_left = False
    if not hand_closed_thumb_left(hand_landmarks):
        thumb_down_left = False

    for finger in fingers_idx:
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[finger].y:
            thumb_down_left = False
    return thumb_down_left


def is_thumb_down_right(hand_landmarks):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_DIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP
    ]
    thumb_is_down_right = True

    for finger in fingers_idx:
        if hand_landmarks.landmark[finger].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
            thumb_is_down_right = False

    if not hand_closed_thumb_right(hand_landmarks, False):
        thumb_is_down_right = False
    for finger in fingers_idx:
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[finger].y:
            thumb_is_down_right = False

    return thumb_is_down_right


def is_thumb_down(results, img):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            thumb_down_left = is_thumb_down_left(hand_landmarks)
            if thumb_down_left:
                print("thumb_down_left")
                return True
            thumb_down_right = is_thumb_down_right(hand_landmarks)
            if thumb_down_right:
                print("thumb down right")
                return True
        return False


def hand_closed_thumb_left(hand_landmarks):
    fingers_idx_TIP = [
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP
    ]

    fingers_idx_PIP = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.PINKY_PIP
    ]

    for finger_TIP, finger_PIP in zip(fingers_idx_TIP, fingers_idx_PIP):
        if hand_landmarks.landmark[finger_TIP].x >= hand_landmarks.landmark[finger_PIP].x:
            return False

    return True


def hand_closed_thumb_right(hand_landmarks, checkIndexFinger):
    fingers_idx_TIP = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP
    ]

    fingers_idx_PIP = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.PINKY_PIP
    ]

    for finger_TIP, finger_PIP in zip(fingers_idx_TIP, fingers_idx_PIP):
        if finger_TIP == 8 and checkIndexFinger:
            continue
        if hand_landmarks.landmark[finger_TIP].x < hand_landmarks.landmark[finger_PIP].x:
            return False

    return True


def index_finger_raised_to_left(results, img):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )
            index_finger_left = is_index_finger_showing_left(hand_landmarks)
            if index_finger_left and hand_closed_thumb_left(hand_landmarks):
                return True
    return False


def index_finger_raised_to_right(results, img):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )
            index_finger_right = is_index_finger_showing_right(hand_landmarks)
            if index_finger_right and hand_closed_thumb_right(hand_landmarks, True):
                return True
    return False


def is_index_finger_showing_left(hand_landmarks):
    fingers_idx = [
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP,
        mp_hands.HandLandmark.THUMB_TIP
    ]

    diff = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x - hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_DIP].x
    q = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y - hand_landmarks.landmark[
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    if q > 0.1:
        return False
    if diff <= 0.04:
        return False

    for finger in fingers_idx:
        if hand_landmarks.landmark[finger].x >= hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x:
            return False
        if is_thumb_down_left(hand_landmarks):
            return False
    return True


def is_index_finger_showing_right(hand_landmarks):
    fingers_idx = [
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP,
        mp_hands.HandLandmark.THUMB_TIP
    ]
    diff = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x - hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_TIP].x

    if diff <= 0.02:
        return False

    q = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y - hand_landmarks.landmark[
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    if q > 0.1:
        return False

    for finger in fingers_idx:
        if hand_landmarks.landmark[finger].x <= hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x:
            return False

    return True


def right_index_closed():
    if (mp_hands.HandLandmark.INDEX_FINGER_TIP.x > mp_hands.HandLandmark.INDEX_FINGER_PIP and

            mp_hands.HandLandmark.INDEX_FINGER_TIP < mp_hands.HandLandmark.WRIST.x):
        return False

    return True


def left_index_closed():
    if (mp_hands.HandLandmark.INDEX_FINGER_TIP.x > mp_hands.HandLandmark.INDEX_FINGER_PIP and

            mp_hands.HandLandmark.INDEX_FINGER_TIP < mp_hands.HandLandmark.WRIST.x):
        return False

    return True


def startDetection(controller):
    capture = cv2.VideoCapture(0)

    while True:
        ret, img = capture.read()

        if not ret:
            continue

        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hand.process(rgb_frame)

        thumb_is_up = is_thumb_up(results, img)
        if thumb_is_up:
            controller.submitFormInputs()
            print("thumb up!")

        thumb_is_down = is_thumb_down(results, img)
        if thumb_is_down:
            controller.clearBrowserFormInputs()
            print("thumb is down")

        index_finger_shown_left = index_finger_raised_to_left(results, img)
        if index_finger_shown_left:
            controller.stepBackInBrowserForm()
            print("index finger raised left")

        index_finger_shown_right = index_finger_raised_to_right(results, img)
        if index_finger_shown_right:
            print("index finger raised right")
            controller.stepForwardInBrowserForm()

        cv2.imshow('Hand Recognition', img)
        cv2.waitKey(0)

    capture.release()
    cv2.destroyAllWindows()
