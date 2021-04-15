import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .unit_control import unit_control
from .custom_toggle import custom_toggle

def control_panel(unit_id, title, is_master=False, checked=False):
    """Generate unit control layout with buttons, and power indicators"""
    control_panel_div = html.Div(
        id=f"control-panel-{unit_id}",
        children=[
            html.Div(
                style={"box-shadow": "1px 2px 3px 0px #00000040"},
                className="d-flex flex-column justify-content-center",
                children=[
                    html.Div(
                        children=[
                            html.H4(title),
                        ]
                    ),
                    dbc.Row(
                        # className="d-flex flex-row",
                        no_gutters=True,
                        justify="start",
                        children=[
                            dbc.Col(
                                width=6,
                                children=[
                                    html.Div(  # rx strength div
                                        style={"height": "106px", "margin-right": "6px", "box-shadow": "1px 2px 3px 0px #00000040"},
                                        className="d-flex flex-column no-pad-l-10",
                                        children=[
                                            html.Div(
                                                className="mr-5",
                                                children=[
                                                    html.P("RX Power", className="property-title"),
                                                    html.P("0.7415 (-0.89 dBm)", id=f"sfp-rx-power-{unit_id}"),
                                                ]
                                            ),
                                            html.Div(
                                                className="d-flex flex-row",
                                                children=[
                                                    dbc.Progress(id=f"rx-power-bar-{unit_id}", value=25, className="mb-3", style={"height": "38px", "width": "100px"}),
                                                    html.Div(
                                                        # style={"position": "absolute", "top": "40px"},
                                                        children=[
                                                            custom_toggle(id=f"led-slider-{unit_id}", checked=checked, label="LED"),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(  # motor state
                                width=3,
                                children=[
                                    html.Div(
                                        style={"height": "106px", "box-shadow": "1px 2px 3px 0px #00000040"},
                                        className="no-pad-l-10",
                                        children=[
                                            html.P("Motor X", className="property-title"),
                                            html.P("-1509", id=f"motor-coord-x-{unit_id}"),
                                            html.P("Motor Y", className="property-title"),
                                            html.P("-2125", id=f"motor-coord-y-{unit_id}")
                                        ]
                                    )
                                    # TODO add desired position after clicks on button
                                ]
                            )
                        ]
                    ),
                    dbc.Row(
                        no_gutters=True,
                        children=[
                            dbc.Col(
                                width=9,
                                children=[
                                    html.Div(
                                        style={"height": "110px", "margin-top": "6px", "box-shadow": "1px 2px 3px 0px #00000040"},
                                        children=[
                                            unit_control(unit_id, is_master, checked) 
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            # html.Div(
            #     style={"position": "relative", "left": "0%"},
            #     children=[
                    
            #     ]
            # )
        ]
    )

    return control_panel_div