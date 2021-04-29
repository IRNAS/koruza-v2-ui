"""
Dashboard layout contents:
* camera stream from device the code is running on
* "master" and "slave" unit control blocks and rx power indicators
"""

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

###################### Dashboard Layout ######################

def dashboard_layout(led_data, calibration_data, mode):

    if mode == "master":
        self_interval = dcc.Interval(id="n-intervals-update-master-info", interval=1000, n_intervals=0)
        slave_interval = dcc.Interval(id="n-intervals-update-slave-info", interval=5000, n_intervals=0)
    if mode == "slave":
        self_interval = dcc.Interval(id="n-intervals-update-master-info", interval=1000, n_intervals=0)
        slave_interval = None

    return dbc.Container(
        id="main-layout",
        className="float-left",
        style={"padding-right": "10px", "padding-left": "10px"},
        children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            Keyboard(id="keyboard"),
            # dcc.Interval(id="n-intervals-update-master-info", interval=1000, n_intervals=0),
            # dcc.Interval(id="n-intervals-update-slave-info", interval=30000, n_intervals=0),
            self_interval,
            slave_interval,
            dcc.ConfirmDialog(id="confirm-homing-dialog-master", message="Are you sure you want to start homing?"),
            dcc.ConfirmDialog(id="confirm-homing-dialog-slave", message="Are you sure you want to start homing?"),
            dbc.Row(  # single bootstrap row
                children=[
                    dbc.Col(
                        xs=12,  # put content in columns when viewing on small devices
                        sm=12,
                        md=6,
                        lg=6,
                        children=[
                            camera_display(calibration_data, src=VIDEO_STREAM_SRC)
                        ]
                    ),
                    dbc.Col(
                        xs=12,
                        sm=12,
                        md=4,
                        lg=4,
                        children=[
                            html.Div(
                                style={"margin-top": "28px"},
                                children=[
                                    control_panel("master", "Primary Unit", is_master=True, checked=led_data)  # master unit controls and transmit power indicator
                                ]
                            ),
                            html.Div(
                                style={"margin-top": "30px"},
                                children=[
                                    control_panel("slave", "Secondary Unit", is_master=False, checked=led_data)  # slave unit controls and transmit power indicator
                                ]
                            )
                        ]
                    )
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        html.Div("", style={"height": "70px"})  # hack to enable scrolling past footer - TODO find a cleaner solution
                    )
                ]
            )
        ]
    )
