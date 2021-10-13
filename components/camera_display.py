import time
import logging
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from ..app import app

from ..components.custom_toggle import custom_toggle

log = logging.getLogger()

def camera_display(src, zoom_data, zoom_level):
    """Generate video stream div with overlay"""

    camera_div = html.Div(
        children=[
            html.Div(
                id="camera-container",
                className="d-flex flex-column align-items-center mt-5",
                children=[
                    html.Div(
                        className="video-container",
                        children=[ 
                            html.Img(src=f"{src}?{time.time()}", id="video-stream-container", className="video-container"),
                            html.Img(src=app.get_asset_url(f"markers/marker_{zoom_level}.png?{time.time()}"), id="calibration-img-container", className="calibration-overlay-container")
                        ]
                    )
                ]
            ),
            custom_toggle(id="camera-zoom-toggle", checked=zoom_data, label="Zoom", style={"text-align": "center"}, className="mt-4 camera-zoom-div", delayed=True, label_left_offset="6px")
        ]
    )
    return camera_div