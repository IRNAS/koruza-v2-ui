# KORUZA-V2-PRO
# 
# =================
# GRAPHICAL USER INTERFACE
# =================
# 
# 
# run with sudo python3 -m koruza_v2.koruza_v2_ui.index

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import logging
import xmlrpc.client

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from .app import server
from .app import app

# Import callbacks
from .callbacks import KoruzaGuiCallbacks

# Import custom components
from .components.header import header
from .components.footer import footer

# Import custom layouts
from .layouts.info_layout import info_layout
from .layouts.dashboard_layout import dashboard_layout
from .layouts.landing_page_layout import landing_page_layout

from ..src.constants import KORUZA_MAIN_PORT
from ..src.config_manager import get_config

log = logging.getLogger()

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Koruza Graphical User Interface</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header(),
    html.Div(id='page-content'),
])

config = get_config()["device_mgmt"]
ch = config["channel"]
mode = config[ch]["mode"]

client = xmlrpc.client.ServerProxy(f"http://localhost:{KORUZA_MAIN_PORT}", allow_none=True)
KoruzaGuiCallbacks(client, mode).callbacks()

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    calibration_data = client.get_calibration_data()
    led_data = client.get_led_data()
   
    # layouts implemented in the future
    # if pathname == "/setup":  
    #     return layout_setup_wizard
    # if pathname == "/info":
    #     return info_layout
    if pathname == "/dashboard":
        return dashboard_layout(led_data, calibration_data, mode)  # pass configs to layout
    else:
        return landing_page_layout

if __name__ == '__main__':
    hostname = "0.0.0.0"
    port = "80"

    app.run_server(
        port=port,
        debug=False,
        host=hostname
    )
