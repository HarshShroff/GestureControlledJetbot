# Gesture Controlled Jetbot

This repository contains two scripts for controlling a Jetbot: `jetbot_side.py` for the Jetbot side and `client_side.py` for the client side. These scripts enable the Jetbot to be controlled using hand gestures.

## Dependencies

- For `jetbot_side.py`:
  - jetbot
  - traitlets
  - ipywidgets
  - opencv-python

- For `client_side.py`:
  - cv2
  - mediapipe
  - time
  - socket

## jetbot_side.ipynb

### Overview

`jetbot_side.ipynb` establishes a connection between the Jetbot's camera and a display widget, allowing for real-time streaming. It listens for client inputs and moves the Jetbot accordingly. The script uses the Jetbot library for robot control and IPython widgets for displaying the camera feed.

### Usage

1. Run `jetbot_side.ipynb` on the Jetbot.
2. Run `client_side.py` on a device with a camera.

## client_side.py

### Overview

`client_side.py` uses OpenCV, Mediapipe, and a socket connection to control a robot using hand gestures. It connects to the Jetbot via a specified IP and port, capturing hand gestures from the camera feed. The detected gestures determine the commands sent to the Jetbot through the socket connection.

### Usage

1. Run `client_side.py` on a device with a camera.
2. Adjust the `HOST` variable to the Jetbot's IP.
3. Perform hand gestures in front of the camera to control the Jetbot.

## Hand Gestures


| Forward | Backward | Short Left Turn |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/forward.png" alt="Forward" width="100%">|  <img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/backward.png" alt="Backward" width="100%">|<img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/sleft.png" alt="Short Left Turn" width="100%">


| Short Right Turn | Long Left Turn | Long Right Turn |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/sright.png" alt="Forward" width="100%">|  <img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/lleft.png" alt="Backward" width="100%">|<img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/lright.png" alt="Short Left Turn" width="100%">


### Demo Video

[<img src="https://github.com/HarshShroff/GestureControlledJetbot/blob/main/docs/imgs/cover.png">](https://drive.google.com/file/d/1hnb25JeQzMP0U4jyhdVHA5woU9TRMHZe/preview)


Feel free to explore and use these scripts to enhance your Jetbot experience. If you encounter any issues or have suggestions, please open an issue or pull request. Happy coding!
