# KORUZA-V2-PRO
# 
# =================
# GRAPHICAL USER INTERFACE
# =================
# 
# 
# run with sudo python3 -m koruza_v2.koruza_v2_ui.index

import dash
import socket
import logging
import xmlrpc.client

from flask import request
from threading import Lock

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
from .layouts.calibration_layout import calibration_layout

from ..src.config_manager import get_config
from ..src.constants import KORUZA_MAIN_PORT
from ..src.camera_util import get_set_zoom

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
local_version = config["version"]
local_unit_mode = mode
remote_unit_mode = "secondary" if mode == "primary" else mode

# get local ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_unit_ip = s.getsockname()[0]
s.close()

lock = Lock()

client = xmlrpc.client.ServerProxy(f"http://localhost:{KORUZA_MAIN_PORT}", allow_none=True)
koruza_callbacks = KoruzaGuiCallbacks(client, mode, lock)
koruza_callbacks.init_dashboard_callbacks()
koruza_callbacks.init_info_layout_callbacks()
koruza_callbacks.init_calibration_callbacks()

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    lock.acquire()
    try:
        calibration_data = client.get_calibration()
    except Exception as e:
        logging.warning(f"Error trying to get calibration data: {e}")
        calibration_data = {}
    lock.release()
    
    lock.acquire()
    try:
        led_data = client.get_led_data()
    except Exception as e:
        logging.warning(f"Error trying to get led data: {e}")
        led_data = None
    lock.release()

    lock.acquire()
    try:
        remote_unit_led_data = client.issue_remote_command("get_led_data", ())
    except Exception as e:
        logging.warning(f"Error trying to get remote unit led data: {e}")
        remote_unit_led_data = None
    lock.release()

    # TODO add zoom level with calibration, change image according to that
    lock.acquire()
    try:
        zoom_data = client.get_zoom_data()
    except Exception as e:
        logging.warning(f"Error trying to get zoom data: {e}")
        zoom_data = None
    lock.release()

    sfp_data = {}
    lock.acquire()
    try:
        sfp_data["local"] = client.get_sfp_diagnostics()
    except Exception as e:
        sfp_data["local"] = {}
    if sfp_data["local"] is None:
        sfp_data["local"] = {}
    lock.release()
    
    lock.acquire()
    try:
        sfp_data["remote"] = client.issue_remote_command("get_sfp_diagnostics", ())
    except Exception as e:
        sfp_data["remote"] = {}
    if sfp_data["remote"] is None:
        sfp_data["remote"] = {}
    lock.release()

    remote_unit_id = "Not Set"
    lock.acquire()
    try:
        remote_unit_id = client.issue_remote_command("get_unit_id", ())
    except Exception as e:
        pass
    lock.release()

    remote_version = "Not Set"
    lock.acquire()
    try:
        remote_version = client.issue_remote_command("get_unit_version", ())
    except Exception as e:
        pass
    lock.release()

    current_camera_config = {}
    lock.acquire()
    try:
        current_camera_config = client.get_current_camera_config()
    except Exception as e:
        pass
    lock.release()

    camera_config = {}
    lock.acquire()
    try:
        camera_config = client.get_camera_config()
    except Exception as e:
        pass
    lock.release()

    curr_calib = {}
    lock.acquire()
    try:
        curr_calib = client.get_current_calibration()
    except Exception as e:
        pass
    lock.release()

    # layouts implemented in the future
    # if pathname == "/setup":  
    #     return layout_setup_wizard
    if pathname == "/calibration":
        # update camera based on requested layout
        try:
            client.focus_on_marker(curr_calib.get("calibration", {}).get("offset_x", 360), curr_calib.get("calibration", {}).get("offset_y", 360), current_camera_config.get("IMG_P", 1.0), current_camera_config)
        except Exception as e:
            print(f"Failed to focus on marker: {e}")
        return calibration_layout(curr_calib.get("calibration", {}))
    if pathname == "/info":
        return info_layout(mode, sfp_data, local_unit_id, remote_unit_id, local_unit_ip, remote_unit_ip, local_unit_mode, remote_unit_mode, local_version, remote_version)
    if pathname == "/dashboard":
        print(f"Current calibration data: {calibration_data}")
        zoom_factor = 1 if zoom_data is False else calibration_data.get("calibration", {}).get("zoom_level", False)
        if zoom_data:
            try:
                client.focus_on_marker(calibration_data.get("calibration", {}).get("offset_x", 360), calibration_data.get("calibration", {}).get("offset_y", 360), camera_config.get("IMG_P", 1.0), camera_config)
            except Exception as e:
                print(f"Failed to focus on marker: {e}")
        else:
            try:
                client.update_camera_config(None, 0, 0, 1)
            except Exception as e:
                print(f"Failed to update camera config: {e}")
        return dashboard_layout(led_data, remote_unit_led_data, mode, local_unit_ip, remote_unit_ip, zoom_data, zoom_factor)  # pass configs to layout
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
