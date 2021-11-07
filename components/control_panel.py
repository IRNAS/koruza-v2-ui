import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from .unit_control import unit_control
from .custom_toggle import custom_toggle
from .rx_indicator import rx_indicator

def control_panel(unit, title, is_master=False, checked=False, alignment_enabled=False):
    """Generate unit control layout with buttons, power indicator and motor positions"""
    
    control_panel_div = html.Div(
        id=f"control-panel-{unit}",
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
                                                        style={"width": "75%"},
                                                        children=[
                                                            html.P("RX Power", className="property-title"),
                                                            html.P("0.0000 mW (-40.0 dBm)", id=f"sfp-rx-power-{unit}", className="property-value"),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        style={"width": "25%"},
                                                        children=[
                                                            custom_toggle(id=f"led-slider-{unit}", checked=checked, label="LED", style={"margin-top": "4px"}),
                                                        ]
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                id=f"rx-bar-container-{unit}",
                                                children=[
                                                    rx_indicator(id=unit, class_name="")
                                                ]
                                            )
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
                                            html.P("0", id=f"motor-coord-x-{unit}", className="property-value"),
                                            html.P("Motor Y", className="property-title"),
                                            html.P("0", id=f"motor-coord-y-{unit}", className="property-value")
                                        ]
                                    )
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
                                    unit_control(unit, is_master, checked, alignment_enabled) 
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    return control_panel_div