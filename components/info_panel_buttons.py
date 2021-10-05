
import dash_bootstrap_components as dbc
import dash_html_components as html

def info_panel_buttons(unit):
    if unit == "local":
        button = dbc.Button(
            html.Span("Restore Calibration", style={"font-size": "18px"}),
            id="btn-restore-calib",
            className="align-self-center control-btn", 
            style={"width": "190px", "margin-top": "10px"},
            # style=style, 
            size="lg",
            n_clicks=0,
            color="#00aacf"
        )
    if unit == "remote":
        button = html.Div("",
            style={"margin-top": "52px"}
        )

    return button