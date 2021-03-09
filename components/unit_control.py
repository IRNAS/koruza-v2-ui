import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .control_button import control_button
from .custom_toggle import custom_toggle

def unit_control(unit_id):
    """Returns unit control div"""
    return html.Div(
        className="d-flex flex-direction-row mt-2",
        children=[
            html.Div(
                style={"position": "relative", "width": "110px"},
                children=[
                    # dbc.DropdownMenu(
                    #     label="Speed",
                    #     id=f"steps-dropdown-{unit_id}",
                    #     style={"position": "absolute", "top": "38%"},
                    #     bs_size="lg",
                    #     children=[
                    #         dbc.DropdownMenuItem(id=f"steps-1-btn-{unit_id}", children="1", style={"font-size": "initial"}, n_clicks=0),
                    #         dbc.DropdownMenuItem(divider=True),
                    #         dbc.DropdownMenuItem(id=f"steps-10-btn-{unit_id}", children="10", style={"font-size": "initial"}, n_clicks=0),
                    #         dbc.DropdownMenuItem(divider=True),
                    #         dbc.DropdownMenuItem(id=f"steps-100-btn-{unit_id}", children="100", style={"font-size": "initial"}, n_clicks=0),
                    #         dbc.DropdownMenuItem(divider=True),
                    #         dbc.DropdownMenuItem(id=f"steps-1000-btn-{unit_id}", children="1000", style={"font-size": "initial"}, n_clicks=0)
                    #     ]
                    # )
                    dcc.Dropdown(
                        id=f"steps-dropdown-{unit_id}",
                        placeholder="Steps",
                        style={"position": "absolute", "top": "38%", "width": "110px"},
                        options=[
                            {"label": "1", "value": 1},
                            {"label": "10", "value": 10},
                            {"label": "100", "value": 100},
                            {"label": "1000", "value": 1000}
                        ],
                        #value=1,
                        clearable=False
                    )
                ]
            ),
            html.Div(
                id=f"unit-control-{unit_id}",
                style={"position": "relative", "height": "118px", "width": "118px", "left": "5%"},
                children=[
                    control_button(arrow_direction="up", id=f"motor-control-btn-up-{unit_id}", style={"position": "absolute", "top": "2%", "left": "35%"}),
                    control_button(arrow_direction="left", id=f"motor-control-btn-left-{unit_id}", style={"position": "absolute", "left": "0%", "top": "37%"}),
                    control_button(arrow_direction="right", id=f"motor-control-btn-right-{unit_id}", style={"position": "absolute", "right": "0%", "top": "37%"}),
                    control_button(arrow_direction="down", id=f"motor-control-btn-down-{unit_id}", style={"position": "absolute", "bottom": "33%", "left": "35%"}),
                    #control_button(arrow_direction="center", id=f"motor-control-btn-center-{unit_id}", style={"position": "absolute", "bottom": "35%", "left": "35%"})
                ]
            ),
            html.Div(
                style={"position": "relative", "left": "10%", "width": "40px"}, 
                children=[
                    control_button(arrow_direction="center", id=f"motor-control-btn-center-{unit_id}", style={"position": "absolute", "top": "37%"}),
                ]
            ),
            html.Div(  # LED control
                style={"position": "relative", "left": "10%", "width": "40px"},
                children=[
                    html.Div(
                        style={"position": "absolute", "top": "40px"},
                        children=[
                            custom_toggle(id=f"led-slider-{unit_id}"),
                            html.P("LEDs", style={"position": "absolute", "left": "16px"})
                        ]
                    )
                ]
            )
        ]
    )