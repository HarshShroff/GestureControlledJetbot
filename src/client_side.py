"""
Author: Harsh Shroff
Date: 12/23/2023

This script uses OpenCV, Mediapipe, and a socket connection to control a robot using hand gestures.

Dependencies:
- cv2
- mediapipe
- time
- socket
"""

import cv2
import mediapipe as mp
import time
import socket

# Set the IP and Port for the socket connection
HOST = "10.200.142.80"  # jetbot's IP
PORT = 12001

# Open the camera
cap = cv2.VideoCapture(1)

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize variables for finger tracking and commands
fingers_right = []
fingers_left = []
hand_count = 0
command_count = 0
command_to_call = ''
string_command = ''
last_command = ''
start_time = 0
p_time, c_time = 0, 9
counta = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    print("Trying to connect")
    s.connect((HOST, PORT))
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (640, 480))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        # Check for found hands
        if results.multi_hand_landmarks:
            counta += 1

            # Adds thumb and palm of the hand(s) found
            for hand_lms in results.multi_hand_landmarks:
                for landmark_id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if hand_count == 0:
                        if landmark_id == 0 or landmark_id == 4:
                            fingers_left.append(lm)
                            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
                            # cv2.arrowedLine(img, , cy, (255, 0, 255), cv2.FILLED)
                    else:
                        if landmark_id == 0 or landmark_id == 4:
                            fingers_right.append(lm)
                            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

                hand_count = 1
            hand_count = 0
        if counta % 10 == 0:

            # check if there are two hands in the image
            if fingers_right and fingers_left:

                # Determining whether the thumbs are leveled with, above, or below the base of the palm
                # This determines which command should later be sent through the socket
                if fingers_right[1].y < (fingers_right[0].y - 0.1):
                    if fingers_left[1].y < (fingers_left[0].y - 0.1):
                        command_to_call = 'w'
                        command_count += 1
                        string_command = "BOTH THUMBS UP"
                        print("Both UP")
                    elif fingers_left[1].y > (fingers_left[0].y + 0.1):
                        command_to_call = 'a'
                        command_count += 1
                        string_command = "RIGHT UP & LEFT DOWN"
                        print("Right UP   Left DOWN")
                elif fingers_right[1].y > (fingers_right[0].y + 0.1):
                    if fingers_left[1].y > (fingers_left[0].y + 0.1):
                        command_to_call = 's'
                        command_count += 1
                        string_command = "BOTH THUMBS DOWN"
                        print("Both DOWN")
                    elif fingers_left[1].y < (fingers_left[0].y - 0.1):
                        command_to_call = 'd'
                        command_count += 1
                        string_command = "RIGHT DOWN & LEFT UP"
                        print("Right DOWN   Left UP")
     
                elif fingers_right[1].x > (fingers_right[0].x + 0.1):
                    if fingers_left[1].x < (fingers_left[0].x + 0.1):
                        command_to_call = 'o'
                        command_count += 1
                        string_command = "BOTH THUMBS FACING"
                        print("Both Facing")

            # If only one hand is present in the image
            elif fingers_left:
                if fingers_left[1].y < (fingers_left[0].y - 0.1):
                    command_to_call = 'c'
                    command_count += 1
                    string_command = "ONE THUMB UP"
                    print("ONE THUMB UP")
                elif fingers_left[1].y > (fingers_left[0].y + 0.1):
                    command_to_call = 'x'
                    command_count += 1
                    string_command = "ONE THUMB DOWN"
                    print("ONE THUMB DOWN")

        # Counts the times the same finger combination is present in a row
        if last_command != command_to_call:
            command_count = 1
            last_command = command_to_call

        # Send the command through the socket when found a specified amount of times
        if command_to_call == 'c' or command_to_call == 'x':
            if command_count == 2:
                print("Sending ")
                s.sendto(command_to_call.encode(), (HOST, PORT))
                command_count = 0
        else:
            if command_count == 2:
                print("Sending ")
                s.sendto(command_to_call.encode(), (HOST, PORT))
                command_count = 0

        # Calculating fps
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        flipped = cv2.flip(img, 1)
        cv2.putText(flipped, "FPS: " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (100, 150, 100), 2)
        cv2.putText(flipped, "Last command sent: " + string_command, (200, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (100, 150, 100), 2)

        # Reset the found fingers
        fingers_right = []
        fingers_left = []
        cv2.imshow('Hand Steering', flipped)
        if cv2.waitKey(1) == 27:
            break
    if cv2.waitKey(1) == 27:
        break

s.close()
cap.release()
cv2.destroyAllWindows()