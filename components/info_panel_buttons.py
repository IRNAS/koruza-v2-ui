
import dash_bootstrap_components as dbc
import dash_html_components as html

def info_panel_buttons(unit):
    if unit == "local":
        buttons = html.Div(
            className="mt-3",
            children=[
                dbc.Button(
                    html.Span("Update Unit", style={"font-size": "18px"}),
                    id="btn-update-unit",
                    className="align-self-center control-btn",
                    style={"width": "120px", "margin-top": "10px", "margin-left": "10px"},
                    size="lg",
                    n_clicks=0,
                    color="#00aacf"
                )
            ]
        )
    if unit == "remote":
        buttons = html.Div("",
            style={"margin-top": "70px"}
        )

    return buttons