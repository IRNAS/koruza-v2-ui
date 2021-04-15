import dash_bootstrap_components as dbc
import dash_html_components as html

def control_button(arrow_direction, id, style={}):
    img_src = None
    if arrow_direction == "up":
        img_src = "../assets/icons/arrow_up_big.png"
    elif arrow_direction == "down":
        img_src = "../assets/icons/arrow_down_big.png"
    elif arrow_direction == "right":
        img_src = "../assets/icons/arrow_right_big.png"
    elif arrow_direction == "left":
        img_src = "../assets/icons/arrow_left_big.png"
    # elif arrow_direction == "center":
    #     img_src = "../assets/icons/plus-circle.svg"

    icon = None
    if img_src is not None:
        icon = html.Img(src=img_src, style={"vertical-align": "middle"}),
    else:
        icon = html.Span(arrow_direction, style={"font-weight": "bold", "font-size": "16px"})
    return dbc.Button(
        icon,
        id=id, 
        className="align-self-center control-btn", 
        style=style, 
        size="lg",
        n_clicks=0
    )