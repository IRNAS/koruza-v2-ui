import socket
import json
import dash
import math
import numpy as np
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_extensions import Keyboard

# import custom components
from ..components.custom_toggle import custom_toggle
#from components.control_button import control_button
from ..components.signal_indicator import signal_indicator
from ..components.control_panel import control_panel
from ..components.functions import generate_marker
from ..components.camera_display import camera_display

#### TODO MOVE TO CONSTANTS ####
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
LOCALHOST = s.getsockname()[0]
s.close()
PORT = 8080
VIDEO_STREAM_SRC = f"http://{LOCALHOST}:{PORT}/?action=stream"

SQUARE_SIZE = 18

###################### Dashboard Layout ######################
"""
___________________
-------------------
|   |             |
|   |             |
|   |             |
|   |             |
-------------------
"""


def dashboard_layout(camera_config, calibration_config):
    return dbc.Container(
        id="main-layout",
        className="float-left",
        # fluid=True,
        style={"padding-right": "10px", "padding-left": "10px"},
        children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            Keyboard(id="keyboard"),
            dcc.Interval(id="n-intervals-update-master-info", interval=1000, n_intervals=0),
            dcc.Interval(id="n-intervals-update-slave-info", interval=1000, n_intervals=0),
            dcc.ConfirmDialog(id="confirm-homing-dialog-master", message="Are you sure you want to start homing?"),
            dcc.ConfirmDialog(id="confirm-homing-dialog-slave", message="Are you sure you want to start homing?"),
            dbc.Row(  # single bootstrap row
                children=[
                    dbc.Col(
                        width=6,
                        children=[
                            camera_display(calibration_config, src=VIDEO_STREAM_SRC)
                        ]
                    ),
                    dbc.Col(
                        width=4,
                        # md=6,
                        children=[
                            html.Div(
                                style={"margin-top": "28px"},
                                children=[
                                    control_panel("master", "Main Unit", is_master=True, checked=camera_config["led"])  # master unit controls and transmit power indicator
                                ]
                            ),
                            html.Div(
                                style={"margin-top": "30px"},
                                children=[
                                    control_panel("slave", "Slave - not functional - WIP", is_master=False, checked=camera_config["led"])  # slave unit controls and transmit power indicator
                                ]
                            )
                            # dbc.Row(  # unit control section
                            #     justify="between",
                            #     children=[
                            #         dbc.Col(
                            #         )
                            #     ]
                            # ),
                            # dbc.Row(  # unit control section
                            #     justify="between",
                            #     children=[
                            #         dbc.Col(
                            #         )
                            #     ]
                            # )
                        ]
                    )
                ]
            ),
        ]
    )
