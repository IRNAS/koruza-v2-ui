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

def dashboard_layout(led_data, remote_unit_led_data, mode, local_unit_ip, remote_unit_ip, zoom_data):

    if mode == "primary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = dcc.Interval(id="n-intervals-update-remote-info", interval=1000, n_intervals=0)
        local_control = html.Div(
            style={"margin-top": "28px"},
            children=[
                control_panel(unit="local", title=f"Primary Unit - {local_unit_ip}", is_master=True, checked=led_data)  # primary unit controls and transmit power indicator
            ]
        )
        remote_control = html.Div(
            style={"margin-top": "30px"},
            children=[
                control_panel(unit="remote", title=f"Secondary Unit - {remote_unit_ip}", is_master=False, checked=remote_unit_led_data)  # secondary unit controls and transmit power indicator
            ]
        )
    if mode == "secondary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = None
        local_control = html.Div(
            style={"margin-top": "28px"},
            children=[
                # NOTE: we set unit_id to primary, as this is the primary control panel, we change the title however
                control_panel(unit="local", title=f"Secondary Unit - {local_unit_ip}", is_master=False, checked=led_data)  # primary unit controls and transmit power indicator
            ]
        )
        remote_control = None

    return dbc.Container(
        id="main-layout",
        className="float-left",
        style={"padding-right": "10px", "padding-left": "10px"},
        children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            Keyboard(id="keyboard"),
            local_interval,
            remote_interval,
            dcc.ConfirmDialog(id="confirm-homing-dialog-local", message="Are you sure you want to start homing?"),
            dcc.ConfirmDialog(id="confirm-homing-dialog-remote", message="Are you sure you want to start homing?"),
            dcc.ConfirmDialog(id="confirm-align-dialog-local", message="Are you sure you want to start automatic alignment?"),
            dbc.Row(  # single bootstrap row
                children=[
                    dbc.Col(
                        xs=12,  # put content in columns when viewing on small devices
                        sm=12,
                        md=6,
                        lg=6,
                        children=[
                            camera_display(VIDEO_STREAM_SRC, zoom_data)
                        ]
                    ),
                    dbc.Col(
                        xs=12,
                        sm=12,
                        md=4,
                        lg=4,
                        children=[
                            local_control,
                            remote_control
                        ]
                    )
                ]
            )
        ]
    )
