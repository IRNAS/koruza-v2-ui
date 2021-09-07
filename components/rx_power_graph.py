import numpy as np
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc

def rx_power_graph(unit_id):
    """
    Generate rx power graph

    TODO: Enable zoom on x axis, when zoomed in display more data points
    TODO: Figure out how much data to display. last 10 mins? 1 datapoint every 30 seconds?

    """

    return html.Div(
        dcc.Graph(
            id=f"rx-power-graph-{unit_id}",
            config={
                # "modeBarButtonsToAdd": [ "drawrect" ],
                "displayModeBar": False,
                # "modeBarButtonsToRemove": [ "autoScale2d", "pan2d", "zoom2d", "zoomIn2d", "zoomOut2d", "resetScale2d" ],
                # "showAxisDragHandles": False,
                "displaylogo": False,
                "editable": False
            },
            figure={
                "data": [
                    {
                        "type": "line",
                        "x": [],
                        "y": []
                    }
                ],
                "layout": {
                    "xaxis": {
                        "showticklabels": True,
                        "ticks": "",
                        "showgrid": False,
                        "zeroline": False,
                        "fixedrange": True,
                    },
                    "yaxis": {
                        "showticklabels": True,
                        "ticks": "outside",
                        "showgrid": True,
                        "zeroline": False,
                        "fixedrange": False,
                    },
                    "paper_bgcolor": "rgba(255, 0, 0, 0.0)",
                    "plot_bgcolor": "rgba(255, 0, 0, 0.0)",
                    "margin": {
                        "t": 0,
                        # "b": 0,
                        "l": 30,
                        "r": 10
                    },
                    "clickmode": "event",
                    "hovermode": "closest",
                    "newshape": {
                        "line": {
                            "color": "#ff0000",
                            "opacity": "1.0"
                        }
                    }
                }
            }
        )
    )
   