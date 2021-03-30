import socket

import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_extensions import Keyboard

# import custom components
from .components.custom_toggle import custom_toggle
#from components.control_button import control_button
from .components.signal_indicator import signal_indicator
from .components.unit_control import unit_control

#### TODO MOVE TO CONSTANTS ####
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
LOCALHOST = s.getsockname()[0]
s.close()
PORT = 8080
VIDEO_STREAM_SRC = f"http://{LOCALHOST}:{PORT}/?action=stream"
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

def generate_control_layout():
    """Camera layout containing real time video, mode selection and granularity selection"""
    control_layout = html.Div(
        id="control-display-div",
        className="border-round",
        children=[
            dbc.Row(
                #id="camera-control-row",
                no_gutters=True,
                align="center",
                justify="space-between",
                children=[
                    # dbc.Col(
                    #     width=4,
                    #     children=[
                    #         html.Span("Steps: "),
                    #         dbc.ButtonGroup(
                    #             children=[
                    #                 dbc.Button(html.Span("1", style={"font-size": "initial"}), id="steps-1-btn", size="lg"),
                    #                 dbc.Button(html.Span("10", style={"font-size": "initial"}), id="steps-10-btn", size="lg"),
                    #                 dbc.Button(html.Span("100", style={"font-size": "initial"}), id="steps-100-btn", size="lg"),
                    #                 dbc.Button(html.Span("1000", style={"font-size": "initial"}), id="steps-1000-btn", size="lg")
                    #             ]
                    #         )
                    #     ]
                    # ),
                    # dbc.Col(
                    #     width=8,
                    #     className="d-flex flex-row align-items-top justify-content-between",
                    #     children=[
                    #         html.Div(
                    #             children=[
                    #                 html.P("Unit Serial Number", className="property-title"),
                    #                 html.P("0046", id="unit-serial-number")
                    #             ]
                    #         ),
                    #         html.Div(
                    #             children=[
                    #                 html.P("IP Address", className="property-title"),
                    #                 html.P("192.168.13.148", id="unit-ip-address")
                    #             ]
                    #         ),
                    #         html.Div(
                    #             children=[
                    #                 html.P("SFP Serial Number", className="property-title"),
                    #                 html.P("H800S003993", id="sfp-serial-number")
                    #             ]
                    #         ),
                    #         html.Div(
                    #             children=[
                    #                 html.P("TX Wavelength", className="property-title"),
                    #                 html.P("1550nm", id="sfp-wavelength")
                    #             ]
                    #         )
                    #     ]
                    # )
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            generate_camera_display_layout()
                        ]
                    )
                ]
            )
        ]   
    )

    return control_layout

def generate_unit_control_layout(unit_id, title, is_master=False):
    """Generate unit control layout with buttons, and power indicators"""
    unit_control_div = html.Div(
        id=f"unit-control-container-{unit_id}",
        children=[
            html.Div(
                className="d-flex flex-column justify-content-center",
                children=[
                    html.Div(
                        children=[
                            html.H4(title),
                        ]
                    ),
                    # html.Div(
                    #     children=[
                    #         html.Div(
                    #             className="d-flex flex-direction-row",
                    #             children=[
                    #                 html.Div(
                    #                     style={"width": "150px"},
                    #                     children=[
                    #                         html.P("Unit Serial Number", className="property-title"),
                    #                         html.P("0046", id="unit-serial-number")
                    #                     ]
                    #                 ),
                    #                 html.Div(
                    #                     style={"width": "150px"},
                    #                     className="ml-4",
                    #                     children=[
                    #                         html.P("SFP Serial Number", className="property-title"),
                    #                         html.P("H800S003993", id="sfp-serial-number")
                    #                     ]
                    #                 )
                    #             ]
                    #         ),
                    #         html.Div(
                    #             className="d-flex flex-direction-row",
                    #             children=[
                    #                 html.Div(
                    #                     style={"width": "150px"},
                    #                     children=[
                    #                         html.P("IP Address", className="property-title"),
                    #                         html.P("192.168.13.148", id="unit-ip-address")
                    #                     ]
                    #                 ),
                    #                 html.Div(
                    #                     style={"width": "150px"},
                    #                     className="ml-4",
                    #                     children=[
                    #                         html.P("TX Wavelength", className="property-title"),
                    #                         html.P("1550nm", id="sfp-wavelength")
                    #                     ]
                    #                 )
                    #             ]
                    #         )
                    #     ]
                    # ),
                    html.Div(
                        className="d-flex flex-row",
                        children=[
                            html.Div(
                                children=[
                                    html.Div(  # rx strength div
                                        #style={"flex-direction": "row"},
                                        className="d-flex",
                                        children=[
                                            html.Div(
                                                className="mr-5",
                                                children=[
                                                    html.P("RX Power", className="property-title"),
                                                    html.P("0.7415 (-0.89 dBm)", id=f"sfp-rx-power-{unit_id}"),
                                                ]
                                            ),
                                            #signal_indicator(f"rx-signal-{unit_id}", "good", "four-bars")  # chane bar to linear bar
                                            dbc.Progress(id=f"rx-power-bar-{unit_id}", value=25, className="mb-3", style={"height": "38px", "width": "100px"}) 
                                        ]
                                    ),
                                    # html.Div(  # tx strength div
                                    #     className="d-flex",
                                    #     #style={"flex-direction": "d-inline-flex",
                                    #     children=[
                                    #         html.Div(
                                    #             className="mr-5",
                                    #             children=[
                                    #                 html.P("TX Power", className="property-title"),
                                    #                 html.P("0.4313 (-3.63 dBm)", id=f"sfp-tx-power-{unit_id}"),
                                    #             ]
                                    #         ),
                                    #         signal_indicator(f"tx-signal-{unit_id}", "good", "four-bars")
                                    #     ]
                                    # )

                                ]
                            ),
                            html.Div(  # motor state
                                style={"position": "relative", "left": "12%"},
                                children=[
                                    html.P("Motor X", className="property-title"),
                                    html.P("-1509", id=f"motor-coord-x-{unit_id}"),
                                    html.P("Motor Y", className="property-title"),
                                    html.P("-2125", id=f"motor-coord-y-{unit_id}")

                                    # TODO add desired position after clicks on button
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                style={"position": "relative", "left": "0%"},
                children=[
                    unit_control(unit_id, is_master) 
                ]
            )
            # html.Div(
            #     id=f"unit-control-{unit_id}",
            #     children=[
            #         control_button(arrow_direction="up", id="motor-control-up-btn"),
            #         control_button(arrow_direction="left", id="motor-control-left-btn"),
            #         control_button(arrow_direction="right", id="motor-control-right-btn"),
            #         control_button(arrow_direction="down", id="motor-control-down-btn")
            #     ]
            # )
        ]
    )

    return unit_control_div

def generate_camera_display_layout():
    """Generate camera display with control buttons"""
    camera_div = html.Div(
        id="camera-container",
        #style={"display": "flex", "flex-direction": "column"},
        className="d-flex flex-column align-items-center mt-5",
        children=[
            
            html.Div(
                #style={"display": "flex", "flex-direction": "row"},
                #className="d-flex flex-row",
                #justify="center",
                #align="center",
                children=[
                    html.Img(src=VIDEO_STREAM_SRC, id="video-stream-container", style={"height":"512px"}),
                ]
            ),
        ]
    )
    return camera_div
   
layout_dashboard = dbc.Container(
    id="main-layout",
    #className="float-left",
    style={"padding-right": "10px", "padding-left": "10px"},
    children=[
        dbc.Row(  # single bootstrap row
            children=[
                html.Div(id="hidden-div", style={"display": "none"}),
                Keyboard(id="keyboard"),
                dcc.Interval(id="n-intervals-update-master-info", interval=500, n_intervals=0),
                dcc.Interval(id="n-intervals-update-slave-info", interval=500, n_intervals=0),
                dcc.ConfirmDialog(id="confirm-homing-dialog-master", message="Are you sure you want to start homing?"),
                dcc.ConfirmDialog(id="confirm-homing-dialog-slave", message="Are you sure you want to start homing?"),
                dbc.Col(  # camera section with device information and control
                    width=10,
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        generate_control_layout()
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(  # unit control section
                            justify="between",
                            children=[
                                dbc.Col(
                                    children=[
                                        generate_unit_control_layout("master", "Master", is_master=True)  # master unit controls and transmit power indicator
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        generate_unit_control_layout("slave", "Slave - not functional - WIP")  # slave unit controls and transmit power indicator
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

###################### END Dashboard Layout ######################

###################### 404 Page ######################
no_page = html.Div([ 
    html.P(["404 Page not found"])
    ], className="no-page")