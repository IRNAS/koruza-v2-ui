"""KORUZA V2 UI Footer class"""

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def footer():
    """Creates footer"""
    
    navbar = dbc.Navbar(
        fixed="bottom",
        style={"height": "43px"},
        children=[
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            width=6,
                            children=[
                                dbc.NavbarBrand("© 2020 KORUZA. ALL RIGHTS RESERVED | Sitemap", className="ml-2", style={"color": "#898989"})
                            ]
                        )
                    ],
                    align="center",
                    justify="center",
                    no_gutters=True,
                ),
                href="http://www.koruza.net/",
                target="_blank"
            )
        ],
        color="#43474d"
    )
    return navbar