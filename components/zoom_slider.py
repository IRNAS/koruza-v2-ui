import dash_core_components as dcc
import dash_html_components as html

def zoom_slider(zoom_level):
    return html.Div(
        children=[
            html.Span("Camera Zoom", style={"font-size": "26px"}),
            dcc.Slider(
                className="mt-3",
                persistence=True,
                persistence_type="memory",
                id='camera-zoom-slider',
                updatemode="mouseup",
                min=1,
                max=21,
                step=1,
                value=zoom_level,
                marks={
                    1: {"label": "1x", "style": {"font-size": "14px"}},
                    2: {"label": "2x", "style": {"font-size": "14px"}},
                    3: {"label": "3x", "style": {"font-size": "14px"}},
                    5: {"label": "5x", "style": {"font-size": "14px"}},
                    7: {"label": "7x", "style": {"font-size": "14px"}},
                    9: {"label": "9x", "style": {"font-size": "14px"}},
                    11: {"label": "11x", "style": {"font-size": "14px"}},
                    13: {"label": "13x", "style": {"font-size": "14px"}},
                    15: {"label": "15x", "style": {"font-size": "14px"}},
                    17: {"label": "17x", "style": {"font-size": "14px"}},
                    19: {"label": "19x", "style": {"font-size": "14px"}},
                    21: {"label": "21x", "style": {"font-size": "14px"}}
                }
            )
        ]
    )