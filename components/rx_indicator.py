import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def rx_indicator(id, class_name):
    """Generate rx power indicator"""
    
    indicator = html.Div(
        id=f"rx-power-bar-{id}",
        className=f"signal-strength {class_name}",
        children=[
            html.Div(className="bar bar-1"),
            html.Div(className="bar bar-2"),
            html.Div(className="bar bar-3"),
            html.Div(className="bar bar-4"),
            html.Div(className="bar bar-5"),
            html.Div(className="bar bar-6"),
            html.Div(className="bar bar-7"),
            html.Div(className="bar bar-8"),
            html.Div(className="bar bar-9")
        ]
    )

    return indicator