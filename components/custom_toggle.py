import dash_html_components as html
import dash_bootstrap_components as dbc

def custom_toggle(id, checked, label, style):
    """Returns custom toggle switch"""
    return html.Div(
        style=style,
        children=[
            dbc.FormGroup(
                children=[
                    dbc.Label(
                        className="switch",
                        children=[
                            dbc.Checkbox(
                                id=id,
                                checked=checked
                            ),
                            html.Span(className="slider-toggle round")
                        ]
                    )
                ],
                check=True
            ),
            html.P(children=label, style={"position": "relative", "left": "16px"}, className="property-value")
        ]
    )