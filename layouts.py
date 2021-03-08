import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import custom components
from components.custom_toggle import custom_toggle
#from components.control_button import control_button
from components.signal_indicator import signal_indicator
from components.unit_control import unit_control

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
                    dbc.Col(
                        width=4,
                        children=[
                            html.Span("Steps: "),
                            dbc.ButtonGroup(
                                children=[
                                    dbc.Button(html.Span("1", style={"font-size": "initial"}), id="steps-1-btn", size="lg"),
                                    dbc.Button(html.Span("10", style={"font-size": "initial"}), id="steps-10-btn", size="lg"),
                                    dbc.Button(html.Span("100", style={"font-size": "initial"}), id="steps-100-btn", size="lg"),
                                    dbc.Button(html.Span("1000", style={"font-size": "initial"}), id="steps-1000-btn", size="lg")
                                ]
                            )
                        ]
                    ),
                    dbc.Col(
                        width=8,
                        className="d-flex flex-row align-items-top justify-content-between",
                        children=[
                            html.Div(
                                children=[
                                    html.P("Unit Serial Number", className="property-title"),
                                    html.P("0046", id="unit-serial-number")
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P("IP Address", className="property-title"),
                                    html.P("192.168.13.148", id="unit-ip-address")
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P("SFP Serial Number", className="property-title"),
                                    html.P("H800S003993", id="sfp-serial-number")
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P("TX Wavelength", className="property-title"),
                                    html.P("1550nm", id="sfp-wavelength")
                                ]
                            )
                        ]
                    )
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

def generate_unit_control_layout(unit_id, title):
    """Generate unit control layout with buttons, and power indicators"""
    unit_control_div = html.Div(
        id=f"unit-control-container-{unit_id}",
        children=[
            html.Div(
                className="d-flex flex-column justify-content-between",
                children=[
                    html.Div(
                        children=[
                            html.H4(title),
                        ]
                    ),
                    html.Div(
                        className="d-flex flex-row justify-content-between",
                        children=[
                            html.Div(
                                children=[
                                    html.Div(  # rx strength div
                                        #style={"flex-direction": "row"},
                                        className="d-flex",
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.P("RX Power", className="property-title"),
                                                    html.P("0.7415 (-0.89 dBm)", id=f"sfp-rx-power-{unit_id}"),
                                                ]
                                            ),
                                            signal_indicator(f"rx-signal-{unit_id}", "good", "four-bars")
                                        ]
                                    ),
                                    html.Div(  # tx strength div
                                        className="d-flex",
                                        #style={"flex-direction": "d-inline-flex",
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.P("TX Power", className="property-title"),
                                                    html.P("0.4313 (-3.63 dBm)", id=f"sfp-tx-power-{unit_id}"),
                                                ]
                                            ),
                                            signal_indicator(f"tx-signal-{unit_id}", "good", "four-bars")
                                        ]
                                    )

                                ]
                            ),
                            html.Div(  # motor state
                                children=[
                                    html.P("Motor X", className="property-title"),
                                    html.P("-1509", id=f"motor-coord-x-{unit_id}"),
                                    html.P("Motor Y", className="property-title"),
                                    html.P("-2125", id=f"motor-coord-y-{unit_id}")
                                ]
                            ),
                            html.Div(  # LED control
                                children=[
                                    custom_toggle(id=f"led-slider-{unit_id}"),
                                    html.Span("LEDs")
                                ]
                            )

                        ]
                    )
                ]
            ),
            html.Div(
                style={"position": "relative", "left": "36%"},
                children=[
                    unit_control(unit_id) 
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
                className="d-flex flex-row",
                #justify="center",
                #align="center",
                children=[
                    html.Img(src="/assets/koruza-temp.png", id="video-stream-container", style={"width":"100%"}),
                ]
            ),
        ]
    )
    return camera_div
   
layout_dashboard = dbc.Container(
    id="main-layout",
    className="float-left",
    children=[
        dbc.Row(  # single bootstrap row
            children=[
                html.Div(id="hidden-div", style={"display": "none"}),
                dcc.Interval(id="n-intervals-update-master-info", interval=500, n_intervals=0),
                dcc.Interval(id="n-intervals-update-slave-info", interval=500, n_intervals=0),
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
                            children=[
                                dbc.Col(
                                    children=[
                                        generate_unit_control_layout("master", "Master")  # master unit controls and transmit power indicator
                                    ]
                                ),
                                dbc.Col(
                                    children=[
                                        generate_unit_control_layout("slave", "Slave")  # slave unit controls and transmit power indicator
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