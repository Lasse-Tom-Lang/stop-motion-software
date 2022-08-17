import PySimpleGUI as sg
import cv2
import os
import WindowManager

cam = cv2.VideoCapture(0)

fps = 1 / 60

mainWindow = WindowManager.mainWindow()

while True:
  event, values = mainWindow.read(timeout=fps)
  if (event == sg.WIN_CLOSED):
    break
  ret, frame = cam.read()
  imgbytes=cv2.imencode('.png', frame)[1].tobytes()
  mainWindow["-CAMERAVIEW-"].update(data=imgbytes, subsample=frame.shape[1] // 500)
  match event:
    case "-TAKEIMAGE-":
      continue

mainWindow.close()