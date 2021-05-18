import dash_html_components as html
import dash_bootstrap_components as dbc

from ..components.rx_power_graph import rx_power_graph

def unit_info_panel(unit_id):
    """Info panel containing info on unit"""

    return html.Div(
        className="flex-direction-column",
        children=[
            html.Div("Unit Serial Number", className="property-title"),
            html.Div("0046", id="unit-serial-number"),
            html.Div("SFP Serial Number", className="property-title"),
            html.Div("H800S003993", id="sfp-serial-number"),
            html.Div("IP Address", className="property-title"),
            html.Div("192.168.13.148", id="unit-ip-address"),
            html.Div("TX Wavelength", className="property-title"),
            html.Div("1550nm", id="sfp-wavelength"),
            html.Div("TX Power", className="property-title"),
            html.Div("0.5928 (-2.27 dBm)", id="tx-power"),
            html.Div("Rx Power", className="property-title"),
            html.Div("0.0002 (-36.99 dBm)", id="rx-power"),
            rx_power_graph(unit_id),
        ]
    )