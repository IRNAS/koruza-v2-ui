import time
import logging
import visdcc
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from ..components.custom_toggle import custom_toggle

from .functions import generate_marker
from ...src.constants import SQUARE_SIZE

log = logging.getLogger()

def camera_display(calibration_data, src, zoom_data):
    """Generate video stream div with overlay"""

    print(f"calib data: {calibration_data}")

    x_pts = []
    y_pts = []
    for x in range(0, 360):
        for y in range(0, 360):
            x_pts.append(x * 2)
            y_pts.append(y * 2)

    marker_lb_rt = None
    marker_lt_rb = None

    try:
        if zoom_data:
            marker_lb_rt, marker_lt_rb = generate_marker(360, 360, SQUARE_SIZE)  # set marker to center of image
        else:
            marker_lb_rt, marker_lt_rb = generate_marker(calibration_data["calibration"]["offset_x"], calibration_data["calibration"]["offset_y"], SQUARE_SIZE)
    except Exception as e:
        log.warning(f"An exception occured when trying to create camera overlay marker: {e}")

    camera_div = html.Div(
        children=[
            visdcc.Run_js("javascript"),  # run javascript to refresh page on demand
            html.Div(
                id="camera-container",
                className="d-flex flex-column align-items-center mt-5",
                children=[
                    html.Div(
                        className="video-container",
                        children=[
                            html.Img(src=f"{src}?{time.time()}", id="video-stream-container", className="video-container", style={"absolute": "relative", "top": "0px", "left": "0px"}),
                            dcc.Graph(
                                id="camera-overlay",
                                className="graph-container",
                                config={
                                    "displayModeBar": False,
                                    "displaylogo": False,
                                    "editable": False
                                },

                                # NOTE TODO this is still kinda slow, figure out a better way to do this
                                figure={
                                    "data": [
                                        {
                                            "x": x_pts,
                                            "y": y_pts,
                                            "marker": {
                                                "color": "rgba(255, 0, 0, 0.0)"
                                            }
                                        }
                                    ],
                                    "layout": {
                                        "xaxis": {
                                            "showticklabels": False,
                                            "ticks": "",
                                            "showgrid": False,
                                            "zeroline": False,
                                            "fixedrange": True,
                                        },
                                        "yaxis": {
                                            "showticklabels": False,
                                            "ticks": "",
                                            "showgrid": False,
                                            "zeroline": False,
                                            "fixedrange": True,
                                        },
                                        "paper_bgcolor": "rgba(255, 0, 0, 0.0)",
                                        "plot_bgcolor": "rgba(255, 0, 0, 0.0)",
                                        "margin": {
                                            "t": 0,
                                            "b": 0,
                                            "l": 0,
                                            "r": 0
                                        },
                                        "clickmode": "event",
                                        "hovermode": "closest",
                                        "newshape": {
                                            "line": {
                                                "color": "#ff0000",
                                                "opacity": "1.0"
                                            }
                                        },
                                        "shapes": [marker_lb_rt, marker_lt_rb]
                                    },
                                }
                            )
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