import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from .functions import generate_marker
from ...src.constants import SQUARE_SIZE
from ...src.camera_util import calculate_marker_pos, calculate_zoom_area_position

def calibration_display(src, calibration_data):
    x_pts = []
    y_pts = []

    marker_lb_rt = None
    marker_lt_rb = None

    num_pts = 720

    marker_x = calibration_data["calibration"]["offset_x"]
    marker_y = calibration_data["calibration"]["offset_y"]

    marker_lb_rt, marker_lt_rb = generate_marker(marker_x, marker_y, SQUARE_SIZE)  # set marker to center of image

    for x in range(0, num_pts):
        for y in range(0, num_pts):
            x_pts.append(x)
            y_pts.append(y)

    calibration_div = dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.Div(
                        className="d-flex flex-column align-items-center",
                        children=[
                            html.Img(src=f"{src}", id="calibration-stream-container", className="video-container"),
                            dcc.Graph(
                                id="camera-overlay",
                                className="graph-container",
                                config={
                                    "displayModeBar": False,
                                    "displaylogo": False,
                                    "editable": False
                                },
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
        ]
    )
    return calibration_div