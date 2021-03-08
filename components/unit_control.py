import dash_html_components as html
import dash_bootstrap_components as dbc

from .control_button import control_button

def unit_control(unit_id):
    """Returns unit control div"""
    return html.Div(
        id=f"unit-control-{unit_id}",
        style={"position": "relative", "height": "118px", "width": "118px"},
        children=[
            control_button(arrow_direction="up", id=f"motor-control-btn-up-{unit_id}", style={"position": "absolute", "top": "0%", "left": "35%"}),
            control_button(arrow_direction="left", id=f"motor-control-btn-left-{unit_id}", style={"position": "absolute", "left": "0%", "top": "35%"}),
            control_button(arrow_direction="right", id=f"motor-control-btn-right-{unit_id}", style={"position": "absolute", "right": "0%", "top": "35%"}),
            control_button(arrow_direction="down", id=f"motor-control-btn-down-{unit_id}", style={"position": "absolute", "bottom": "0%", "left": "35%"}),
            control_button(arrow_direction="center", id=f"motor-control-btn-center-{unit_id}", style={"position": "absolute", "bottom": "35%", "left": "35%"})
        ]
    )