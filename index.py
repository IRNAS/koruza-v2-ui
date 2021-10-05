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

import socket
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

config = get_config()
link_config = config["link_config"]
ch = link_config["channel"]
mode = link_config[ch]["mode"]
remote_unit_ip = link_config[ch]["remote_unit_addr"]
local_unit_id = config["unit_id"]

# get local ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_unit_ip = s.getsockname()[0]
s.close()

client = xmlrpc.client.ServerProxy(f"http://localhost:{KORUZA_MAIN_PORT}", allow_none=True)
koruza_callbacks = KoruzaGuiCallbacks(client, mode)
koruza_callbacks.init_dashboard_callbacks()
koruza_callbacks.init_info_layout_callbacks()

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    try:
        calibration_data = client.get_calibration()
    except Exception as e:
        logging.warning(f"Error trying to get calibration data: {e}")
        calibration_data = None
    try:
        led_data = client.get_led_data()
    except Exception as e:
        logging.warning(f"Error trying to get led data: {e}")
        led_data = None
   
    sfp_data = {}
    try:
        sfp_data["local"] = client.get_sfp_diagnostics()
    except Exception as e:
        sfp_data["local"] = {}
    if sfp_data["local"] is None:
        sfp_data["local"] = {}
    
    try:
        sfp_data["remote"] = client.issue_remote_command("get_sfp_diagnostics", ())
    except Exception as e:
        sfp_data["remote"] = {}
    if sfp_data["remote"] is None:
        sfp_data["remote"] = {}

    remote_unit_id = ""
    try:
        remote_unit_id = client.issue_remote_command("get_unit_id", ())
    except Exception as e:
        pass

    # layouts implemented in the future
    # if pathname == "/setup":  
    #     return layout_setup_wizard
    if pathname == "/info":
        return info_layout(mode, sfp_data, local_unit_id, remote_unit_id, local_unit_ip, remote_unit_ip)
    if pathname == "/dashboard":
        return dashboard_layout(led_data, calibration_data, mode, local_unit_ip, remote_unit_ip)  # pass configs to layout
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
