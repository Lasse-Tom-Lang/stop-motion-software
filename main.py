import PySimpleGUI as sg
import cv2
import os
import WindowManager

frames = [img[0:-4] for img in os.listdir("frames") if img.endswith(".png")]
frames.sort()

images = [cv2.imread(os.path.join("frames", f"{frame}.png")) for frame in frames]

nextFrame = len(frames)

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

mainWindow = WindowManager.mainWindow(working_ports, frames)
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
    fpsTimeout = 1000 / int(values["-FPS-"])
    fps = int(values["-FPS-"])
  except:
    fpsTimeout = 1000 / 60
    fps = 60
  event, values = mainWindow.read(timeout=fpsTimeout)
  if playing and len(frames) > 0:
    displayFrame = images[currentFrame]
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
      images.append(frame)
      mainWindow["-FRAMES-"].update(frames)
      nextFrame += 1
    case "-FRAMES-":
      selected = int(values["-FRAMES-"][0])
      displayFrame = images[selected]
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
    case "-BEFORE-":
      displayFrame = images[currentFrame]
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
      mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
      currentFrame -= 1
      if (currentFrame < 0):
        currentFrame = len(frames) - 1
    case "-NEXT-":
      displayFrame = images[currentFrame]
      imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
      mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
      mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
      currentFrame += 1
      if (currentFrame == len(frames)):
        currentFrame = 0
    case "-CHANGECAMERA-":
      cam = cv2.VideoCapture(values["-CHANGECAMERA-"])
    case "-RENDER-":
      renderWindow = WindowManager.renderWindow(len(frames))
      height, width, layers = images[0].shape 
      video = cv2.VideoWriter("Video.avi", 0, fps, (width,height))
      a = 0
      for image in images:
        renderWindow.read(timeout=1)
        video.write(image)
        renderWindow["-RENDERPROGRESS-"].UpdateBar(a)
        a = a + 1
      video.release()
      renderWindow.close()

mainWindow.close()