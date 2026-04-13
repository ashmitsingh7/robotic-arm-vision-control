import cv2
import mediapipe as mp
import numpy as np
import socket
import time

# ── TCP Setup (replacing serial) ──────────────────────
ESP_IP = "10.212.176.238"   # ← put this exact IP
PORT   = 1234               # ← already correct
START  = 255
END    = 254

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ESP_IP, PORT))
time.sleep(1)
print("Connected to ESP32 at {}:{}".format(ESP_IP, PORT))

# ── MediaPipe Hands ────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ── Map ratio 0.0–1.0 to servo 0–180 ──────────────────
def map_to_servo(ratio):
    return int(np.clip(ratio * 180, 0, 180))

# ── How raised is a finger (0.0 = down, 1.0 = fully up)
def finger_ratio(lm, tip_id):
    tip_y = lm[tip_id].y
    pip_y = lm[tip_id - 2].y
    mcp_y = lm[tip_id - 3].y
    span  = mcp_y - pip_y + 1e-6
    return float(np.clip((pip_y - tip_y) / span, 0.0, 1.0))

# ── Thumb uses x axis instead of y ────────────────────
def thumb_ratio(lm):
    tip_x = lm[4].x
    ip_x  = lm[3].x
    mcp_x = lm[2].x
    span  = abs(mcp_x - ip_x) + 1e-6
    return float(np.clip((ip_x - tip_x) / span, 0.0, 1.0))

# ── Get all 5 servo values from hand landmarks ─────────
def get_servos_from_hand(hand_lm):
    lm = hand_lm.landmark

    t_ratio = thumb_ratio(lm)
    i_ratio = finger_ratio(lm, 8)
    m_ratio = finger_ratio(lm, 12)
    r_ratio = finger_ratio(lm, 16)
    p_ratio = finger_ratio(lm, 20)

    w = map_to_servo(m_ratio)
    s = map_to_servo(t_ratio)
    e = map_to_servo(i_ratio)
    t = map_to_servo(r_ratio)

    if p_ratio > 0.5:
        g = 180
        gripper_state = "OPEN"
        gripper_color = (0, 255, 0)
    else:
        g = 0
        gripper_state = "CLOSED"
        gripper_color = (0, 0, 255)

    ratios = [t_ratio, i_ratio, m_ratio, r_ratio, p_ratio]
    return w, s, e, t, g, gripper_state, gripper_color, ratios

# ── Draw info on screen ────────────────────────────────
def draw_info(frame, w, s, e, t, g, gripper_state, gripper_color):
    info = [
        ("Shoulder  (Thumb) : {} deg".format(s),                      (160, 80, 255)),
        ("Elbow     (Index) : {} deg".format(e),                      (255, 220, 0)),
        ("Wrist     (Middle): {} deg".format(w),                      (0, 255, 200)),
        ("Turntable (Ring)  : {} deg".format(t),                      (255, 165, 0)),
        ("Gripper   (Pinky) : {} [{}]".format(g, gripper_state),      gripper_color),
    ]
    for i, (text, color) in enumerate(info):
        cv2.putText(frame, text, (10, 40 + i * 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

# ── Draw dots on fingertips ────────────────────────────
def draw_finger_overlay(frame, hand_lm, ratios, gripper_color):
    lm = hand_lm.landmark
    h, fw, _ = frame.shape
    tip_ids = [4,  8,  12, 16, 20]
    labels  = ["T→S","I→E","M→W","R→T","P→G"]
    colors  = [(160,80,255),(255,220,0),(0,255,200),(255,165,0), gripper_color]

    for i, tip_id in enumerate(tip_ids):
        x = int(lm[tip_id].x * fw)
        y = int(lm[tip_id].y * h)
        cv2.circle(frame, (x, y), 13, colors[i], -1)
        cv2.putText(frame, labels[i], (x - 14, y + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1)

# ── Send over TCP — same packet, same 7 bytes ──────────
def send_arm(w, s, e, t, g):
    print("Sending -> W:{} S:{} E:{} T:{} G:{}".format(w, s, e, t, g))
    packet = bytes([START, w, s, e, t, g, END])
    sock.sendall(packet)           # sendall instead of ser.write

# ── Main Loop ──────────────────────────────────────────
cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        hands_results = hands.process(rgb)

        if hands_results.multi_hand_landmarks:
            hand_landmarks = hands_results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            w, s, e, t, g, gripper_state, gripper_color, ratios = get_servos_from_hand(hand_landmarks)

            draw_finger_overlay(frame, hand_landmarks, ratios, gripper_color)
            draw_info(frame, w, s, e, t, g, gripper_state, gripper_color)
            send_arm(w, s, e, t, g)

        else:
            cv2.putText(frame, "Show your hand to the camera!", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.putText(frame, "TCP → {}:{}".format(ESP_IP, PORT),
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

        cv2.imshow("Robotic Arm - WiFi TCP", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopping...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
