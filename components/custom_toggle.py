import dash_html_components as html
import dash_bootstrap_components as dbc

def custom_toggle(id):
    """Returns custom toggle switch"""
    return html.Div(
        dbc.FormGroup(
            children=[
                dbc.Label(
                    className="switch",
                    children=[
                        dbc.Checkbox(
                            id=id,
                            checked=False
                        ),
                        html.Span(className="slider-toggle round")
                    ]
                )
            ],
            check=True
        )
    )