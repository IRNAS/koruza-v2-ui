import logging
import dash_core_components as dcc
import dash_html_components as html

from .functions import generate_marker
from ...src.constants import SQUARE_SIZE

log = logging.getLogger()

def camera_display(calibration_config, src):
    """Generate video stream div with overlay"""

    x_pts = []
    y_pts = []
    for x in range(0, 360):
        for y in range(0, 360):
            x_pts.append(x * 2)
            y_pts.append(y * 2)

    marker_lb_rt = None
    marker_lt_rb = None

    try:
        marker_lb_rt, marker_lt_rb = generate_marker(calibration_config["offset_x"], calibration_config["offset_y"], SQUARE_SIZE)
    except Exception as e:
        log.warning(e)

    camera_div = html.Div(
        id="camera-container",
        className="d-flex flex-column align-items-center mt-5",
        children=[
            html.Div(
                className="video-container",
                children=[
                    html.Img(src=src, id="video-stream-container", className="video-container", style={"absolute": "relative", "top": "0px", "left": "0px"}),
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
    )
    return camera_div