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

def info_layout(mode, sfp_data, unit_id, remote_unit_id, local_unit_ip, remote_unit_ip, local_unit_mode, remote_unit_mode, local_sw_version, remote_sw_version):
    if mode == "primary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = dcc.Interval(id="n-intervals-update-remote-info", interval=1000, n_intervals=0)
        info_panel_local = unit_info_panel("local", local_unit_ip, unit_id, local_unit_mode, local_sw_version, sfp_data.get("local", {}))
        info_panel_remote = unit_info_panel("remote", remote_unit_ip, remote_unit_id, remote_unit_mode, remote_sw_version, sfp_data.get("remote", {}))
        rx_power_graph_local = rx_power_graph("local")
        rx_power_graph_remote = rx_power_graph("remote")
        buttons_local = info_panel_buttons("local")
        buttons_remote = info_panel_buttons("remote")
    if mode == "secondary":
        local_interval = dcc.Interval(id="n-intervals-update-local-info", interval=1000, n_intervals=0)
        remote_interval = None
        info_panel_local = unit_info_panel("local", local_unit_ip, unit_id, local_unit_mode, local_sw_version, sfp_data.get("local", {}))  # koruza is in secodary mode but data is from "primary" as it's local
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
            dcc.ConfirmDialog(id="confirm-update-unit-dialog", message="Check for updates?"),
            dcc.ConfirmDialog(id="update-status-dialog", message="The unit is updating. The unit will restart once the update is finished!"),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            info_panel_local,
                            buttons_local,
                            rx_power_graph_local
                        ]
                    ),
                    dbc.Col(
                        children=[
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