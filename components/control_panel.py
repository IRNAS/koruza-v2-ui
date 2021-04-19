import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .unit_control import unit_control
from .custom_toggle import custom_toggle
from .rx_indicator import rx_indicator

def control_panel(unit_id, title, is_master=False, checked=False):
    """Generate unit control layout with buttons, and power indicators"""
    control_panel_div = html.Div(
        id=f"control-panel-{unit_id}",
        style={"width": "450px", "height": "350px"},
        children=[
            html.Div(
                className="d-flex flex-column justify-content-center",
                children=[
                    html.Div(
                        style={"margin-top": "6px", "margin-left": "16px"},
                        children=[
                            html.H5(title, style={"font-weight": "500", "font-size": "30px"}),
                        ]
                    ),
                    html.Div(
                        className="d-flex flex-row",
                        style={"height": "140px"},
                        children=[
                            html.Div(
                                style={"width": "70%"},
                                children=[
                                    html.Div(  # rx strength div
                                        style={"height": "100%", "margin": "6px"},
                                        className="d-flex flex-column no-pad-l-10 background-koruza div-control-group",
                                        children=[
                                            html.Div(
                                                className="d-flex flex-row",
                                                children=[
                                                    html.Div(
                                                        # className="mr-5",
                                                        style={"width": "75%"},
                                                        children=[
                                                            html.P("RX Power", className="property-title"),
                                                            html.P("0.7415 (-0.89 dBm)", id=f"sfp-rx-power-{unit_id}", className="property-value"),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        # style={"position": "absolute", "top": "40px"},
                                                        style={"width": "25%"},
                                                        children=[
                                                            custom_toggle(id=f"led-slider-{unit_id}", checked=checked, label="LED", style={"margin-top": "4px"}),
                                                        ]
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                id=f"rx-bar-container-{unit_id}",
                                                children=[
                                                    rx_indicator(id=unit_id, class_name="")
                                                ]
                                            )
                                            # dbc.Progress(id=f"rx-power-bar-{unit_id}", value=25, className="mb-3", style={"height": "38px", "width": "100px"}),
                                        ]
                                    )
                                ]
                            ),
                            html.Div(  # motor state
                                style={"width": "30%"},
                                children=[
                                    html.Div(
                                        style={"margin": "6px", "height": "100%"},
                                        className="no-pad-l-10 background-koruza div-control-group",
                                        children=[
                                            html.P("Motor X", className="property-title"),
                                            html.P("-1509", id=f"motor-coord-x-{unit_id}", className="property-value"),
                                            html.P("Motor Y", className="property-title"),
                                            html.P("-2125", id=f"motor-coord-y-{unit_id}", className="property-value")
                                        ]
                                    )
                                    # TODO add desired position after clicks on button
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        style={"width": "100%", "height": "120px", "margin-top": "12px"},
                        children=[
                            html.Div(
                                style={"height": "100%", "margin": "6px"},
                                className="no-pad-l-10 background-koruza div-control-group",
                                children=[
                                    unit_control(unit_id, is_master, checked) 
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    return control_panel_div