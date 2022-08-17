import PySimpleGUI as sg

backgroundColor = "#323232"
elementColor = "#404040"
textColor = "white"

def mainWindow():
  layout = [
    [sg.Image("", key="-FRAME-"), sg.Image("", key="-CAMERAVIEW-")],
    [sg.Button("Take image", key="-TAKEIMAGE-", button_color=(textColor, elementColor))]
  ]
  return sg.Window(
    "Stop motion software",
    layout,
    resizable=True,
    background_color=backgroundColor,
    location=(100, 100)
  )