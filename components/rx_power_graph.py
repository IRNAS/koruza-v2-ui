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
                        "y": [],
                        "line": {
                            # "color": range(-40, 1),
                            # "colorscale": "Hot",
                            "opacity": "1.0"
                        }
                    }
                ],
                "layout": {
                    "xaxis": {
                        "showticklabels": True,
                        "ticks": "",
                        "showgrid": False,
                        "zeroline": False,
                        "fixedrange": False,
                        "range": [-110, 10]
                    },
                    "yaxis": {
                        "showticklabels": True,
                        "ticks": "outside",
                        "showgrid": True,
                        "zeroline": False,
                        "fixedrange": True,
                        "range": [-45, 5],
                        "title": "Rx Power (dBm)"
                    },
                    "paper_bgcolor": "rgba(255, 0, 0, 0.0)",
                    "plot_bgcolor": "rgba(255, 0, 0, 0.0)",
                    "margin": {
                        "t": 20,
                        # "b": 0,
                        "l": 60,
                        "r": 20
                    }
                }
            }
        )
    )
   