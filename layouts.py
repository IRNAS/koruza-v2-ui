import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import custom components
from components.custom_toggle import custom_toggle
from components.control_button import control_button

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

def generate_data_display_layout():
    """Section containing information about the Koruza unit"""
    data_display_layout = html.Div(
        id="data-display-div",
        className="border-round d-flex flex-column",
        #style={"display": "flex", "flex-direction": "column"},
        children=[

            # Unit Identity div
            html.Div(
                id="unit-identity-div",
                className="d-flex flex-column",
                #style={"flex-direction": "column"},
                children=[
                    html.P("Unity Identity", className="section-title-text"),
                    html.P("Serial Number", className="property-title"),
                    html.P("0046", id="unit-serial-number")
                ]
            ),

            # Network status div
            html.Div(
                id="network-status-div",
                className="d-flex flex-column",
                #style={"flex-direction": "column"},
                children=[
                    html.P("Network", className="section-title-text"),
                    html.P("IP Address", className="property-title"),
                    html.P("192.168.13.148", id="unit-ip-address")
                ]
            ),

            # MCU status div
            html.Div(
                id="mcu-status-div",
                className="d-flex flex-column",
                #style={"flex-direction": "column"},
                children=[
                    html.P("MCU Connected", id="mcu-status", className="section-title-text"),
                    html.P("Motor X", className="property-title"),
                    html.P("-1509", id="motor-coord-x"),
                    html.P("Motor Y", className="property-title"),
                    html.P("-2125", id="motor-coord-y")
                ]
            ),

            # SFP status div
            html.Div(
                id="sfp-status-div",
                className="d-flex flex-column",
                #style={"flex-direction": "column"},
                children=[
                    html.P("SFP Connected", id="sfp-status", className="section-title-text"),
                    html.P("Serial Number", className="property-title"),
                    html.P("H800S003993", id="sfp-serial-number"),
                    html.P("TX Wavelength", className="property-title"),
                    html.P("1550nm", id="sfp-wavelength"),
                    html.P("RX Power", className="property-title"),
                    html.P("0.7415 (-0.89 dBm)", id="sfp-rx-power"),
                    html.P("TX Power", className="property-title"),
                    html.P("0.4313 (-3.63 dBm)", id="sfp-tx-power")
                ]
            ),

            # Controls div
            html.Div(
                id="controls-div",
                className="d-flex flex-column",
                #style={"flex-direction": "column"},
                children=[
                    html.P("Controls", className="section-title-text"),
                    dbc.Button("Homing", id="homing-btn", size="lg"),
                    html.Div(
                        className="d-flex flex-row",
                        #style={"flex-direction": "row"},
                        children=[
                            custom_toggle(id="led-slider"),
                            html.Span("LEDs")
                        ]
                    )
                ]
            )
        ]
    )

    return data_display_layout

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
                        width=5,
                        #style={"flex-direction": "row"},
                        children=[
                            html.Span("Mode: "),
                            dbc.ButtonGroup(
                                children=[
                                    dbc.Button(html.Span("None", style={"font-size": "initial"}), id="none-btn", size="lg"),
                                    dbc.Button(html.Span("Movement", style={"font-size": "initial"}), id="movement-btn", size="lg"),
                                    dbc.Button(html.Span("Calibration", style={"font-size": "initial"}), id="calibration-btn", size="lg")
                                ]
                            )
                        ]
                    ),
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
                        width=3,
                        children=[
                            dbc.DropdownMenu(
                                bs_size="lg",
                                label="Survey",
                                children=[
                                    dbc.DropdownMenuItem("Toggle visibility", style={"font-size": "initial"}, id="toggle-overlay-btn"),
                                    dbc.DropdownMenuItem("Reset", style={"font-size": "initial"}, id="reset-overlay-btn")
                                ],
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

def generate_camera_display_layout():
    """Generate camera display with control buttons"""
    camera_div = html.Div(
        id="camera-container",
        #style={"display": "flex", "flex-direction": "column"},
        className="d-flex flex-column align-items-center mt-5",
        children=[
            control_button(arrow_direction="up", id="motor-control-up-btn"),
            html.Div(
                #style={"display": "flex", "flex-direction": "row"},
                className="d-flex flex-row",
                #justify="center",
                #align="center",
                children=[
                    control_button(arrow_direction="left", id="motor-control-left-btn"),
                    html.Img(src="/assets/koruza-temp.png", id="video-stream-container", style={"width":"100%"}),
                    control_button(arrow_direction="right", id="motor-control-right-btn"),
                ]
            ),
            control_button(arrow_direction="down", id="motor-control-down-btn"),
        ]
    )
    return camera_div
   
layout_dashboard = dbc.Container(
    id="main-layout",
    className="float-left",
    children=[
        dbc.Row(  # single bootstrap row
            children=[
                dbc.Col(  # koruza data display
                    width=2,
                    style={"min-width": "190px", "max-width": "190px"},
                    children=[
                        generate_data_display_layout()
                    ]
                ),
                dbc.Col(  # camera section with motor controls
                    width=10,
                    children=[
                        generate_control_layout()
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