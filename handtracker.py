import cv2
import mediapipe as mp
import mediapipe.python.solutions.drawing_styles as drawing_styles

mp_hands = mp.solutions.hands
hand = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


def is_thumb_up(results, img):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP
    ]

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            for finger in fingers_idx:
                if (hand_landmarks.landmark[finger].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                        ):
                    return False

    return True


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
    return (
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_TIP].y and
            hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_MCP].y
            and hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y > hand_landmarks.landmark[
                mp_hands.HandLandmark.THUMB_TIP].y)


def is_thumb_down(results, img):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP
    ]

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            for finger in fingers_idx:
                if (hand_landmarks.landmark[finger].y > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                        or not hand_closed(hand_landmarks)):
                    return False

    return True


def is_index_right(results, img):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_DIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP, mp_hands.HandLandmark.THUMB_TIP
    ]

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            for finger in fingers_idx:
                if (hand_landmarks.landmark[finger].x < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                or not right_index_closed):
                    return False

    return True


def is_index_left(results, img):
    fingers_idx = [
        mp_hands.HandLandmark.INDEX_FINGER_DIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP, mp_hands.HandLandmark.THUMB_TIP
    ]

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      drawing_styles.get_default_hand_landmarks_style(),
                                      drawing_styles.get_default_hand_connections_style()
                                      )

            for finger in fingers_idx:
                if (hand_landmarks.landmark[finger].x > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                       and not left_index_closed()):
                    return False

    return True

#TODO: change hand_closed, so also right hand gets triggerd
def hand_closed(hand_landmarks):
    fingers_idx_TIP = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP
    ]

    fingers_idx_PIP = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.PINKY_PIP
    ]

    for finger_TIP, finger_PIP in zip(fingers_idx_TIP, fingers_idx_PIP):
        print("TIP", hand_landmarks.landmark[finger_TIP].x)
        print("PIP", hand_landmarks.landmark[finger_PIP].x)
        if hand_landmarks.landmark[finger_TIP].x < hand_landmarks.landmark[finger_PIP].x:
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


def startDetection():
    capture = cv2.VideoCapture(0)

    while True:
        ret, img = capture.read()

        if not ret:
            continue

        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hand.process(rgb_frame)

        thumb_is_up = is_thumb_up(results, img)
        if thumb_is_up:
            print("thumb up!")

        thumb_is_down = is_thumb_down(results, img)
        if thumb_is_down:
            print("thumb is down")

        index_is_right = is_index_right(results, img)
        if index_is_right:
            print("index is right")

        index_is_left = is_index_left(results, img)
        if index_is_left:
            print("index is left")

        cv2.imshow('Hand Recognition', img)
        cv2.waitKey(0)

    capture.release()
    cv2.destroyAllWindows()
