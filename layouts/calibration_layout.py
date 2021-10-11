import socket
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from ..components.calibration_display import calibration_display

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
LOCALHOST = s.getsockname()[0]
s.close()
PORT = 8080
VIDEO_STREAM_SRC = f"http://{LOCALHOST}:{PORT}/?action=stream"

def calibration_layout(calibration_data):
    return dbc.Container(
        id="main-layout",
        className="float-left",
        style={"margin-left": "20px"},
        children=[
            dcc.ConfirmDialog(id="confirm-calibration-dialog", message="Are you sure you want to set new calibration?"),
            dcc.ConfirmDialog(id="confirm-zoom-dialog", message="Are you sure you want to change the zoom level?"),
            dbc.Row(  # single bootstrap row
                className="mt-5",
                children=[
                    dbc.Col(
                        xs=12,  # put content in columns when viewing on small devices
                        sm=12,
                        md=7,
                        lg=7,
                        children=[
                            calibration_display(VIDEO_STREAM_SRC, calibration_data)
                        ]
                    ),
                    dbc.Col(
                        style={"text-align": "center"},
                        xs=12,
                        sm=12,
                        md=4,
                        lg=4,
                        children=[
                            html.Div(
                                className="div-control-group",
                                style={"padding-bottom": "24px", "padding-top": "10px"},
                                children=[
                                    html.Div(
                                        children=[
                                            html.Span("Camera Zoom", style={"font-size": "26px"}),
                                            dcc.Slider(
                                                className="mt-3",
                                                persistence=True,
                                                persistence_type="memory",
                                                id='camera-zoom-slider',
                                                updatemode="mouseup",
                                                min=1,
                                                max=20,
                                                step=0.5,
                                                value=calibration_data["calibration"]["zoom_level"],
                                                marks={
                                                    1: {"label": "1x", "style": {"font-size": "14px"}},
                                                    2: {"label": "2x", "style": {"font-size": "14px"}},
                                                    4: {"label": "4x", "style": {"font-size": "14px"}},
                                                    6: {"label": "6x", "style": {"font-size": "14px"}},
                                                    8: {"label": "8x", "style": {"font-size": "14px"}},
                                                    10: {"label": "10x", "style": {"font-size": "14px"}},
                                                    12: {"label": "12x", "style": {"font-size": "14px"}},
                                                    14: {"label": "14x", "style": {"font-size": "14px"}},
                                                    16: {"label": "16x", "style": {"font-size": "14px"}},
                                                    18: {"label": "18x", "style": {"font-size": "14px"}},
                                                    20: {"label": "20x", "style": {"font-size": "14px"}}
                                                }
                                            )
                                        ]
                                    ),
                                    dbc.Button(
                                        html.Span("Confirm Calibration", style={"font-size": "18px"}),
                                        style={"width": "200px", "margin-top": "20px"},
                                        id="calibration-btn", 
                                        className="align-self-center control-btn", 
                                        size="lg",
                                        n_clicks=0,
                                        color="#00aacf"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )