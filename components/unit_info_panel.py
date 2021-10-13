import dash_html_components as html
import dash_bootstrap_components as dbc

def unit_info_panel(unit, unit_ip, unit_id, unit_mode, sw_version, sfp_data):
    """Info panel containing info on unit"""

    print(f"SFP data passed to unit info panel: {sfp_data}")

    return html.Div(
        className="flex-direction-column",
        children=[
            html.Div(
                className="mt-3",
                children=[
                    html.Div("Unit Serial Number", className="property-title"),
                    html.Div(unit_id, id=f"unit-serial-number-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("Unit Mode", className="property-title"),
                    html.Div(unit_mode, id=f"unit-mode-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("Unit Software Version", className="property-title"),
                    html.Div(sw_version, id=f"unit-sw-version-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("SFP Serial Number", className="property-title"),
                    html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("serial_num", "/"), id=f"sfp-serial-number-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("IP Address", className="property-title"),
                    html.Div(unit_ip, id=f"unit-ip-address-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("TX Wavelength", className="property-title"),
                    html.Div(sfp_data.get("sfp_0", {}).get("module_info", {}).get("wavelength", "/"), id=f"sfp-wavelength-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("TX Power", className="property-title"),
                    html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power", "/"), id=f"tx-power-{unit}", style={"font-size": "18px"})
                ]
            ),
            html.Div(
                className="mt-3",
                children=[
                    html.Div("Rx Power", className="property-title"),
                    html.Div(sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power_dBm", "/"), id=f"rx-power-{unit}", style={"font-size": "18px"})
                ]
            )
        ]
    )