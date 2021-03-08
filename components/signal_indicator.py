import dash_html_components as html
import dash_bootstrap_components as dbc

def signal_indicator(id, strength="", bar_count=""):
    """Returns custom toggle switch"""
    return html.Div(
        html.Div(
            id=f"{id}-wrapper",
            className=f"{strength} {bar_count}",
            children=[
                html.Div(
                    id=id,
                    className="signal-bars sizing-box",
                    children=[
                        html.Div(
                            className="first-bar bar"
                        ),
                        html.Div(
                            className="second-bar bar"
                        ),
                        html.Div(
                            className="third-bar bar"
                        ),
                        html.Div(
                            className="fourth-bar bar"
                        ),
                        html.Div(
                            className="fifth-bar bar"
                        )
                    ]
                )
            ]
        )
    )