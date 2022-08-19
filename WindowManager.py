import PySimpleGUI as sg

backgroundColor = "#323232"
elementColor = "#404040"
textColor = "white"

def mainWindow(activCameras):
  layout = [
    [
      sg.Listbox(
        [],
        size=(
          5,
          40
        ),
        expand_y=True,
        background_color=elementColor,
        text_color=textColor,
        sbar_background_color=backgroundColor,
        sbar_arrow_width=0,
        sbar_trough_color=backgroundColor,
        key="-FRAMES-",
        enable_events=True
      ),
      sg.Image(
        "",
        key="-FRAME-"
      ),
      sg.Image(
        "",
        key="-CAMERAVIEW-"
      )
    ],
    [
      sg.Button(
        "<",
        key="-BEFORE-",
        button_color=(
          textColor,
          elementColor
        )
      ),
      sg.Button(
        "Play",
        key="-PLAY-",
        button_color=(
          textColor,
          elementColor
        )
      ),
      sg.Button(
        ">",
        key="-NEXT-",
        button_color=(
          textColor,
          elementColor
        )
      ),
      sg.In(
        60,
        key="-FPS-",
        background_color=elementColor,
        text_color=textColor
      )
    ],
    [
      sg.Button(
        "Take image",
        key="-TAKEIMAGE-",
        button_color=(
          textColor,
          elementColor
        )
      ),
      sg.Checkbox(
        "Show camera",
        True,
        background_color=backgroundColor,
        checkbox_color=elementColor,
        text_color=textColor,
        key="-CAMERAPREVIEW-",
      ),
      sg.Combo(
        activCameras,
        default_value=0,
        background_color=elementColor,
        text_color=textColor,
        button_background_color=elementColor,
        button_arrow_color=textColor,
        change_submits=True,
        key="-CHANGECAMERA-"
      )
    ]
  ]
  return sg.Window(
    "Stop motion software",
    layout,
    resizable=True,
    background_color=backgroundColor,
    location=(0, 0)
  )