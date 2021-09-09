"""
Info layout contents:
* two info panels - "master" and "slave" information
TODO: add features
"""

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ..components.unit_info_panel import unit_info_panel

def info_layout(mode, sfp_data, local_unit_ip, remote_unit_ip):
    if mode == "primary":
        self_interval = dcc.Interval(id="n-intervals-update-primary-info", interval=1000, n_intervals=0)
        secondary_interval = dcc.Interval(id="n-intervals-update-secondary-info", interval=1000, n_intervals=0)
    if mode == "secondary":
        self_interval = dcc.Interval(id="n-intervals-update-primary-info", interval=1000, n_intervals=0)
        secondary_interval = None

    info_layout = dbc.Container(
        id="info-layout",
        style={"padding-right": "10px", "padding-left": "10px"},
        children=[
            self_interval,
            secondary_interval,
            dcc.ConfirmDialog(id="confirm-restore-calibration-dialog", message="Restore calibration to factory default?"),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            unit_info_panel("primary", sfp_data.get("primary", {}), local_unit_ip, remote_unit_ip),
                        ]
                    ),
                    dbc.Col(
                        children=[
                            unit_info_panel("secondary", sfp_data.get("secondary", {}), local_unit_ip, remote_unit_ip)
                        ]
                    )
                ]
            )
        ]
    )

    return info_layout