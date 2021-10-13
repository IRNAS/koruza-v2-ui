import socket
import visdcc
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
            visdcc.Run_js("javascript"),  # run javascript to refresh page on demand
            dcc.ConfirmDialog(id="confirm-calibration-dialog", message="Are you sure you want to set new calibration?"),
            dcc.ConfirmDialog(id="confirm-zoom-dialog", message="Are you sure you want to change the zoom level?"),
            dcc.ConfirmDialog(id="confirm-restore-calibration-dialog", message="Restore calibration to factory default?"),
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
                                                max=21,
                                                step=1,
                                                value=calibration_data["calibration"]["zoom_level"],
                                                marks={
                                                    1: {"label": "1x", "style": {"font-size": "14px"}},
                                                    2: {"label": "2x", "style": {"font-size": "14px"}},
                                                    3: {"label": "3x", "style": {"font-size": "14px"}},
                                                    5: {"label": "5x", "style": {"font-size": "14px"}},
                                                    7: {"label": "7x", "style": {"font-size": "14px"}},
                                                    9: {"label": "9x", "style": {"font-size": "14px"}},
                                                    11: {"label": "11x", "style": {"font-size": "14px"}},
                                                    13: {"label": "13x", "style": {"font-size": "14px"}},
                                                    15: {"label": "15x", "style": {"font-size": "14px"}},
                                                    17: {"label": "17x", "style": {"font-size": "14px"}},
                                                    19: {"label": "19x", "style": {"font-size": "14px"}},
                                                    21: {"label": "21x", "style": {"font-size": "14px"}}
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
                                    ),
                                    dbc.Button(
                                        html.Span("Restore Calibration", style={"font-size": "18px"}),
                                        id="btn-restore-calib",
                                        className="align-self-center control-btn", 
                                        style={"width": "200px", "margin-top": "20px", "margin-left": "20px"},
                                        # style=style, 
                                        size="lg",
                                        n_clicks=0,
                                        color="#00aacf"
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )