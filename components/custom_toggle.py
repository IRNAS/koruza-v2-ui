import dash_html_components as html
import dash_bootstrap_components as dbc

def custom_toggle(id, checked, label, style, className="", delayed=False, label_left_offset="16px"):
    """Creates custom toggle switch"""
    delayed_class = ""
    if delayed:
        delayed_class = "slider-toggle-delayed"
    return html.Div(
        className=className,
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
                            html.Span(className=f"slider-toggle round {delayed_class}")
                        ]
                    )
                ],
                check=True
            ),
            html.P(children=label, style={"position": "relative", "left": label_left_offset}, className="property-value")
        ]
    )