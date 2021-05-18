import dash_bootstrap_components as dbc
import dash_html_components as html

def control_button(arrow_direction, id, style={}):
    """Custom control button with pre-defined assets or custom text"""
    img_src = None
    if arrow_direction == "up":
        img_src = "../assets/icons/arrow-up.png"
    elif arrow_direction == "down":
        img_src = "../assets/icons/arrow-down.png"
    elif arrow_direction == "right":
        img_src = "../assets/icons/arrow-right.png"
    elif arrow_direction == "left":
        img_src = "../assets/icons/arrow-left.png"

    icon = None
    if img_src is not None:
        icon = html.Img(src=img_src, style={"vertical-align": "middle"}),
    else:
        icon = html.Span(arrow_direction, style={"font-size": "28px", "font-weight": "500", "color": "#00aacf"})
    return dbc.Button(
        icon,
        id=id, 
        className="align-self-center control-btn", 
        style=style, 
        size="lg",
        n_clicks=0,
        color="#00aacf"
    )