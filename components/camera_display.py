import time
import logging
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from ..components.custom_toggle import custom_toggle

log = logging.getLogger()

def camera_display(src, zoom_data):
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
                            html.Img(src=f"calibration-{zoom_data}.jpg", id="calibration-img-container")
                        ]
                    )
                ]
            ),
            html.Div(
                className="mt-4 camera-zoom-div",
                style={"text-align": "center"},
                children=[
                    html.Div(
                        children=[
                            dbc.FormGroup(
                                children=[
                                    dbc.Label(
                                        className="switch",
                                        children=[
                                            dbc.Checkbox(
                                                id="camera-zoom-toggle",
                                                checked=zoom_data
                                            ),
                                            html.Span(className="slider-toggle round")
                                        ]
                                    )
                                ],
                                check=True
                            ),
                            html.P(children="Zoom", style={"position": "relative", "left": "6px"}, className="property-value")
                        ]
                    )
                ]
            )
        ]
    )
    return camera_div