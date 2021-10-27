import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .control_button import control_button
from .custom_toggle import custom_toggle

def unit_control(unit, is_master=False, checked=False):
    """Generate unit control div with control buttons, homing button and step selection"""
    align_button = html.Div(id=f"motor-control-btn-align-{unit}")

    if unit == "local":
        arrows = [
            control_button(arrow_direction="W", id=f"motor-control-btn-up-{unit}", style={"position": "absolute", "top": "6%", "left": "35%"}),
            control_button(arrow_direction="A", id=f"motor-control-btn-left-{unit}", style={"position": "absolute", "left": "0%", "top": "48%"}),
            control_button(arrow_direction="D", id=f"motor-control-btn-right-{unit}", style={"position": "absolute", "right": "0%", "top": "48%"}),
            control_button(arrow_direction="S", id=f"motor-control-btn-down-{unit}", style={"position": "absolute", "top": "48%", "left": "35%"})
        ]
    else:
        arrows = [
            control_button(arrow_direction="up", id=f"motor-control-btn-up-{unit}", style={"position": "absolute", "top": "6%", "left": "35%"}),
            control_button(arrow_direction="left", id=f"motor-control-btn-left-{unit}", style={"position": "absolute", "left": "0%", "top": "48%"}),
            control_button(arrow_direction="right", id=f"motor-control-btn-right-{unit}", style={"position": "absolute", "right": "0%", "top": "48%"}),
            control_button(arrow_direction="down", id=f"motor-control-btn-down-{unit}", style={"position": "absolute", "top": "48%", "left": "35%"})
        ]

    if is_master:
        align_button = html.Div(
            style={"position": "relative", "left": "10%"}, 
            children=[
                dbc.Button("Align", id=f"motor-control-btn-align-{unit}", style={"font-size": "28px", "font-weight": "500", "color": "#00aacf", "position": "absolute", "top": "0%", "left": "100%", "height": "42px", "width": "120px", "line-height": "0px"}, className="align-self-center", size="lg", n_clicks=0)
            ]
        )

    return html.Div(
        className="d-flex flex-direction-row",
        children=[
            html.Div(
                style={"position": "relative", "width": "110px", "font-size": "22px", "text-align": "vertical"},
                children=[
                    html.P("STEPS", className="property-title"),
                    dcc.Dropdown(
                        id=f"steps-dropdown-{unit}",
                        placeholder="Steps",
                        style={"position": "absolute", "top": "38%", "width": "110px"},
                        options=[
                            {"label": "1", "value": 1},
                            {"label": "10", "value": 10},
                            {"label": "100", "value": 100},
                            {"label": "1000", "value": 1000}
                        ],
                        value=1000,
                        clearable=False,
                        persistence=True,
                        searchable=False
                    )
                ]
            ),
            html.Div(
                id=f"unit-control-{unit}",
                style={"position": "relative", "height": "118px", "width": "140px", "left": "5%"},
                children=arrows,
            ),
            html.Div(
                style={"position": "relative", "left": "10%"}, 
                children=[
                    dbc.Button("Homing", id=f"motor-control-btn-center-{unit}", style={"font-size": "28px", "font-weight": "500", "color": "#00aacf", "position": "absolute", "top": "48%", "left": "100%", "height": "42px", "width": "120px", "line-height": "0px"}, className="align-self-center", size="lg", n_clicks=0)
                ]
            ),
            align_button
        ]
    )
