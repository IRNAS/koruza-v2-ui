import dash_bootstrap_components as dbc
import dash_html_components as html

def control_button(arrow_direction, id):
    if arrow_direction == "up":
        img_src = "../assets/icons/arrow_up_big.png"
    elif arrow_direction == "down":
        img_src = "../assets/icons/arrow_down_big.png"
    elif arrow_direction == "right":
        img_src = "../assets/icons/arrow_right_big.png"
    elif arrow_direction == "left":
        img_src = "../assets/icons/arrow_left_big.png"

    return dbc.Button(
        html.Img(src=img_src, style={"vertical-align": "middle"}),
        id=id, 
        className="align-self-center", 
        style={"height":"36px", "width":"36px", "padding": "0px"}, 
        size="lg"
    )