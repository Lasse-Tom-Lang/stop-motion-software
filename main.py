import PySimpleGUI as sg
import cv2
import os
import WindowManager

if (not os.path.exists("frames/order.txt")):
  with open("frames/order.txt", "x"):
    pass

with open("frames/order.txt", "r") as orderFile:
  orderText = orderFile.read()
  order = orderText.split(";")
  if (order[0] == ""):
    del order[0]

images = [cv2.imread(os.path.join("frames", f"{frame}.png")) for frame in order]

nextFrame = len(order)

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

mainWindow = WindowManager.mainWindow(working_ports, order)
event, values = mainWindow.read(timeout=1)
mainWindow.maximize()

if (len(images) > 0):
  displayFrame = images[currentFrame]
  imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
  mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
  mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)

cam = cv2.VideoCapture(0)

while True:
  try:
    fpsTimeout = 1000 / int(values["-FPS-"])
    fps = int(values["-FPS-"])
  except:
    fpsTimeout = 1000 / 60
    fps = 60
  event, values = mainWindow.read(timeout=fpsTimeout)
  if (event == sg.WIN_CLOSED):
    break
  if (values["-CAMERAPREVIEW-"]):
    ret, frame = cam.read()
    imgbytes=cv2.imencode('.png', frame)[1].tobytes()
    mainWindow["-CAMERAVIEW-"].update(data=imgbytes, subsample=frame.shape[1] // 500)
  if playing and len(order) > 0:
    displayFrame = images[currentFrame]
    imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
    mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
    mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
    currentFrame += 1
    if (currentFrame == len(order)):
      currentFrame = 0
  match event:
    case "-PLAY-":
      if (len(images) > 0):
        if playing:
          playing = False
          mainWindow["-PLAY-"].update("Play")
        else:
          playing = True
          mainWindow["-PLAY-"].update("Pause")
    case "-TAKEIMAGE-":
      cv2.imwrite(f"frames/{nextFrame}.png",frame)
      order.append(nextFrame)
      images.append(frame)
      mainWindow["-FRAMES-"].update(order)
      nextFrame += 1
    case "-FRAMES-":
      if (len(values["-FRAMES-"]) > 0 and values["-FRAMES-"] != ""):
        selected = order.index(values["-FRAMES-"][0])
        currentFrame = selected
        displayFrame = images[selected]
        imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
        mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
    case "-BEFORE-":
      if (len(images) != 0):
        currentFrame -= 1
        if (currentFrame < 0):
          currentFrame = len(order) - 1
        displayFrame = images[currentFrame]
        imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
        mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
        mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
    case "-NEXT-":
      if (len(images) != 0):
        currentFrame += 1
        if (currentFrame == len(order)):
          currentFrame = 0
        displayFrame = images[currentFrame]
        imagebytes = cv2.imencode('.png', displayFrame)[1].tobytes()
        mainWindow["-FRAME-"].update(data=imagebytes, subsample=displayFrame.shape[1] // 500)
        mainWindow["-FRAMES-"].update(set_to_index=[currentFrame], scroll_to_index=currentFrame)
    case "-CHANGECAMERA-":
      cam = cv2.VideoCapture(values["-CHANGECAMERA-"])
    case "-RENDER-":
      renderWindow = WindowManager.renderWindow(len(order))
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
    case "-DELETEFRAME-":
      if (len(values["-FRAMES-"]) == 1 and values["-FRAMES-"][0] != ""):
        del images[order.index(values["-FRAMES-"][0])]
        os.remove(f"frames/{values['-FRAMES-'][0]}.png")
        del order[order.index(values["-FRAMES-"][0])]
        mainWindow["-FRAMES-"].update(order)
with open("frames/order.txt", "w") as orderFile:
  orderToSave = ""
  for item in order:
    orderToSave = orderToSave + str(item) + ";"
  orderToSave = orderToSave[0:-1]
  orderFile.write(orderToSave)

mainWindow.close()