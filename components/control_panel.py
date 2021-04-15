import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .unit_control import unit_control

def control_panel(unit_id, title, is_master=False, checked=False):
    """Generate unit control layout with buttons, and power indicators"""
    control_panel_div = html.Div(
        id=f"control-panel-{unit_id}",
        children=[
            html.Div(
                className="d-flex flex-column justify-content-center",
                children=[
                    html.Div(
                        children=[
                            html.H4(title),
                        ]
                    ),
                    html.Div(
                        className="d-flex flex-row",
                        children=[
                            html.Div(
                                children=[
                                    html.Div(  # rx strength div
                                        className="d-flex",
                                        children=[
                                            html.Div(
                                                className="mr-5",
                                                children=[
                                                    html.P("RX Power", className="property-title"),
                                                    html.P("0.7415 (-0.89 dBm)", id=f"sfp-rx-power-{unit_id}"),
                                                ]
                                            ),
                                            dbc.Progress(id=f"rx-power-bar-{unit_id}", value=25, className="mb-3", style={"height": "38px", "width": "100px"}) 
                                        ]
                                    )
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
                    unit_control(unit_id, is_master, checked) 
                ]
            )
        ]
    )

    return control_panel_div