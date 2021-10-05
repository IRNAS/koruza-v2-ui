import dash_html_components as html
import dash_bootstrap_components as dbc

def unit_info_panel(unit, unit_ip, unit_id, sw_version, sfp_data):
    """Info panel containing info on unit"""

    print(f"SFP data passed to unit info panel: {sfp_data}")

    return html.Div(
        className="flex-direction-column",
        children=[        
            html.Div("Unit Serial Number", className="property-title"),
            html.Div(unit_id, id=f"unit-serial-number-{unit}"),
            html.Div("Unit Software Version", className="property-title"),
            html.Div(sw_version, id=f"unit-sw-version-{unit}"),
            html.Div("SFP Serial Number", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("serial_num", "/"), id=f"sfp-serial-number-{unit}"),
            html.Div("IP Address", className="property-title"),
            html.Div(unit_ip, id=f"unit-ip-address-{unit}"),
            html.Div("TX Wavelength", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("wavelength", "/"), id=f"sfp-wavelength-{unit}"),
            html.Div("TX Power", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power", "/"), id=f"tx-power-{unit}"),
            html.Div("Rx Power", className="property-title"),
            html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power_dBm", "/"), id=f"rx-power-{unit}"),
        ]
    )