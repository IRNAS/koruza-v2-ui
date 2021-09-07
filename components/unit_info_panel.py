import dash_html_components as html
import dash_bootstrap_components as dbc

from ..components.rx_power_graph import rx_power_graph

def unit_info_panel(unit_id, sfp_data):
    """Info panel containing info on unit"""

    print(f"SFP data passed to unit info panel: {sfp_data}")

    return html.Div(
        className="flex-direction-column",
        children=[
            html.Div("Unit Serial Number", className="property-title"),
            html.Div("0046", id=f"unit-serial-number-{unit_id}"),
            html.Div("SFP Serial Number", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("serial_num", "/"), id=f"sfp-serial-number-{unit_id}"),
            html.Div("IP Address", className="property-title"),
            html.Div("192.168.13.148", id=f"unit-ip-address-{unit_id}"),
            html.Div("TX Wavelength", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("wavelength", "/"), id=f"sfp-wavelength-{unit_id}"),
            html.Div("TX Power", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power", "/"), id=f"tx-power-{unit_id}"),
            html.Div("Rx Power", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power_dBm", "/"), id=f"rx-power-{unit_id}"),
            rx_power_graph(unit_id),
        ]
    )