"""
  The WindowManager creates new windows with PySimpleGUI
"""
import PySimpleGUI as sg

backgroundColor = "#323232"
elementColor = "#404040"
textColor = "white"

def mainWindow(activCameras: list[int], frames: list[int]) -> sg.Window:
  layout = [
    [
      sg.Column(
        [
          [
            sg.Listbox(
              frames,
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
            )
          ]
        ],
        pad=0,
        expand_y=True,
        background_color=backgroundColor
      ),
      sg.Column(
        [
          [
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
              ),
              pad=0,
              border_width=0,
              font="Arial 16"
            ),
            sg.Button(
              "Play",
              key="-PLAY-",
              button_color=(
                textColor,
                elementColor
              ),
              pad=0,
              border_width=0,
              font="Arial 16"
            ),
            sg.Button(
              ">",
              key="-NEXT-",
              button_color=(
                textColor,
                elementColor
              ),
              pad=0,
              border_width=0,
              font="Arial 16"
            ),
            sg.In(
              60,
              key="-FPS-",
              background_color=elementColor,
              text_color=textColor
            ),
            sg.Button(
              "Render",
              key="-RENDER-",
              button_color=(
                textColor,
                elementColor
              )
            )
          ],
          [
            sg.Frame(
              "Frames",
              [
                [
                  sg.Button(
                    "Delete Frame",
                    key="-DELETEFRAME-",
                    button_color=(
                      textColor,
                      elementColor
                    ),
                    font="Arial 12"
                  )
                ]
              ],
              title_color=textColor,
              background_color=backgroundColor,
              font="Arial 20",
              pad=0
            ),
            sg.Frame(
              "Input", 
              [
                [
                  sg.Button(
                    "Take image",
                    key="-TAKEIMAGE-",
                    button_color=(
                      textColor,
                      elementColor
                    ),
                    font="Arial 12"
                  ),
                  sg.Checkbox(
                    "Show camera",
                    True,
                    background_color=backgroundColor,
                    checkbox_color=elementColor,
                    text_color=textColor,
                    key="-CAMERAPREVIEW-",
                    font="Arial 12"
                  ),
                  sg.Combo(
                    activCameras,
                    default_value=0,
                    background_color=elementColor,
                    text_color=textColor,
                    button_background_color=elementColor,
                    button_arrow_color=textColor,
                    change_submits=True,
                    key="-CHANGECAMERA-",
                    font="Arial 12"
                  )
                ]
              ],
              title_color=textColor,
              background_color=backgroundColor,
              font="Arial 20",
              pad=0
            )
          ]
        ],
        pad=1,
        expand_x=True,
        expand_y=True,
        background_color=backgroundColor
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

def renderWindow(frames: int) -> sg.Window:
  layout = [
    [
      sg.ProgressBar(
        frames,
        orientation="horizontal",
        bar_color=(
          "blue",
          elementColor
        ),
        size=(
          50,
          30
        ),
        key="-RENDERPROGRESS-"
      )
    ]
  ]
  return sg.Window(
    "Rendering",
    layout,
    background_color=backgroundColor,
    location=(
      100,
      100
    ),
    disable_close=True,
    no_titlebar=True
  )