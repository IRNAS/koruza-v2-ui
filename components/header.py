"""KORUZA V2 UI Header class, use to navigate between pages"""

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def Header():
    navbar = dbc.Navbar(
        className="pt-0 pb-0 pr-0 pl-0 mb-1",
        children=[
            html.Div(
                className="navbar-collapse collapse",
                style={"background": "rgb(210, 220, 220)"},
                children=[
                    html.Ul(
                        id="nav",
                        className="navbar-nav mr-auto",
                        children=[
                            html.Li(
                                children=[
                                    dbc.NavItem(dbc.NavLink(id="info-navlink", children="KORUZA Link Information", href="/info", active="exact"))
                                ]
                            ),
                            html.Li(
                                children=[
                                    dbc.NavItem(dbc.NavLink(id="dashboard-navlink", children="Unit Dashboard", href="/dashboard", active="exact"))
                                ]
                            ),
                            
                        ]
                    )
                ]
            )
        ]
    )
    return navbar