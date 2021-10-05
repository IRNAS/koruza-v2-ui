"""
Info layout contents:
* two info panels - "primary" and "secondary" unit information
* buttons - reset calibration, update unit
"""

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ..components.rx_power_graph import rx_power_graph
from ..components.unit_info_panel import unit_info_panel
from ..components.info_panel_buttons import info_panel_buttons

def info_layout(mode, sfp_data, unit_id, remote_unit_id, local_unit_ip, remote_unit_ip):
    if mode == "primary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = dcc.Interval(id="n-intervals-update-remote-info", interval=1000, n_intervals=0)
        info_panel_local = unit_info_panel("local", local_unit_ip, unit_id, sfp_data.get("primary", {}))
        info_panel_remote = unit_info_panel("remote", remote_unit_ip, remote_unit_id, sfp_data.get("secondary", {}))
        rx_power_graph_local = rx_power_graph("local")
        rx_power_graph_remote = rx_power_graph("remote")
        buttons_local = info_panel_buttons("local")
        buttons_remote = info_panel_buttons("remote")
    if mode == "secondary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = None
        info_panel_local = unit_info_panel("local", local_unit_ip, unit_id, sfp_data.get("primary", {}))  # koruza is in secodary mode but data is from "primary" as it's local
        info_panel_remote = None
        rx_power_graph_local = rx_power_graph("local")
        rx_power_graph_remote = None
        buttons_local = info_panel_buttons("local")
        buttons_remote = None

    info_layout = dbc.Container(
        id="info-layout",
        style={"padding-right": "10px", "padding-left": "10px"},
        children=[
            local_interval,
            remote_interval,
            dcc.ConfirmDialog(id="confirm-restore-calibration-dialog", message="Restore calibration to factory default?"),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            # unit_info_panel("primary", unit_id, sfp_data.get("primary", {}), local_unit_ip, remote_unit_ip),
                            info_panel_local,
                            buttons_local,
                            rx_power_graph_local
                        ]
                    ),
                    dbc.Col(
                        children=[
                            # unit_info_panel("secondary", remote_unit_id, sfp_data.get("secondary", {}), local_unit_ip, remote_unit_ip)
                            info_panel_remote,
                            buttons_remote,
                            rx_power_graph_remote
                        ]
                    )
                ]
            )
        ]
    )

    return info_layout