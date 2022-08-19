import PySimpleGUI as sg
import cv2
import os
import WindowManager

nextFrame = 0
frames = []
currentFrame = 0
playing = False

is_working = True
dev_port = 0
working_ports = []
while is_working:
  camera = cv2.VideoCapture(dev_port)
  if not camera.isOpened():
    is_working = False
  else:
    is_reading, img = camera.read()
    if is_reading:
      working_ports.append(dev_port)
  dev_port +=1

mainWindow = WindowManager.mainWindow(working_ports)
event, values = mainWindow.read(timeout=1)

cam = cv2.VideoCapture(0)

while True:
  if (values["-CAMERAPREVIEW-"]):
    ret, frame = cam.read()
    imgbytes=cv2.imencode('.png', frame)[1].tobytes()
    mainWindow["-CAMERAVIEW-"].update(data=imgbytes, subsample=frame.shape[1] // 500)
  else:
    mainWindow["-CAMERAVIEW-"].update(data=None)
  try:
    fps = 1000 / int(values["-FPS-"])
  except:
    fps = 1000 / 60
  event, values = mainWindow.read(timeout=fps)
  if playing and len(frames) > 0:
    displayFrame = cv2.imread(f"frames/{currentFrame}.png")
    imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
    mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
    mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
    currentFrame += 1
    if (currentFrame == len(frames)):
      currentFrame = 0
  match event:
    case sg.WIN_CLOSED:
      break
    case "-PLAY-":
      if playing:
        playing = False
      else:
        playing = True
    case "-TAKEIMAGE-":
      cv2.imwrite(f"frames/{nextFrame}.png",frame)
      frames.append(nextFrame)
      mainWindow["-FRAMES-"].update(frames)
      nextFrame += 1
    case "-FRAMES-":
      selected = values["-FRAMES-"][0]
      displayFrame = cv2.imread(f"frames/{selected}.png")
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
    case "-BEFORE-":
      displayFrame = cv2.imread(f"frames/{currentFrame}.png")
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
      mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
      currentFrame -= 1
      if (currentFrame < 0):
        currentFrame = len(frames) - 1
    case "-NEXT-":
      displayFrame = cv2.imread(f"frames/{currentFrame}.png")
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
      mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
      currentFrame += 1
      if (currentFrame == len(frames)):
        currentFrame = 0
    case "-CHANGECAMERA-":
      cam = cv2.VideoCapture(values["-CHANGECAMERA-"])

mainWindow.close()