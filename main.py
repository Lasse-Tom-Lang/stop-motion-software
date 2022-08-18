import PySimpleGUI as sg
import cv2
import os
import WindowManager

cam = cv2.VideoCapture(0)

nextFrame = 0
frames = []
currentFrame = 0
playing = False

mainWindow = WindowManager.mainWindow()
event, values = mainWindow.read(timeout=1)

while True:
  ret, frame = cam.read()
  imgbytes=cv2.imencode('.png', frame)[1].tobytes()
  mainWindow["-CAMERAVIEW-"].update(data=imgbytes, subsample=frame.shape[1] // 500)
  try:
    fps = 1000 / int(values["-FPS-"])
  except:
    fps = 1000 / 60
  event, values = mainWindow.read(timeout=fps)
  if playing and len(frames) > 0:
    displayFrame = cv2.imread(f"frames/{currentFrame}.png")
    imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
    mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
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

mainWindow.close()