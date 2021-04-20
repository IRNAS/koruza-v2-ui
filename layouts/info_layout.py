"""
Info layout contents:
* two info panels - "master" and "slave" information
TODO: add features
"""

import dash_html_components as html
import dash_bootstrap_components as dbc

from ..components.unit_info_panel import unit_info_panel

info_layout = dbc.Container(
    id="info-layout",
    style={"padding-right": "10px", "padding-left": "10px"},
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        unit_info_panel("master"),
                    ]
                ),
                dbc.Col(
                    children=[
                        unit_info_panel("slave")
                    ]
                )
            ]
        )
    ]
)