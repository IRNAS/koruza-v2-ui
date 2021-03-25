import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# run with sudo python3 -m koruza_v2.koruza_v2_ui.index

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from .app import server
from .app import app
from .layouts import layout_dashboard, no_page
from .callbacks import KoruzaGuiCallbacks

from ..koruza_v2_driver.src.motor_driver_wrapper import MotorWrapper
from ..koruza_v2_driver.src.led_driver import LedDriver
from ..koruza_v2_driver.src.sfp_wrapper import SfpWrapper
#import callbacks

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
    html.Div(id='page-content')
])

""" INITS - NOTE THIS IS TEMPORARY - connect all with koruza.py and initi only koruza.py"""
# Init motor driver
motor_driver = None
try:
    motor_driver = MotorWrapper("/dev/ttyAMA0", baudrate=115200, timeout=2)
except Exception as e:
    print("Failed to init Motor Driver")

led_driver = None
try:
    led_driver = LedDriver()
except Exception as e:
    print("Failed to init LED Driver")

sfp_wrapper = None
try:
    sfp_wrapper = SfpWrapper()
except Exception as e:
    print("Failed to init SFP Wrapper")

KoruzaGuiCallbacks(motor_driver, led_driver, sfp_wrapper).callbacks()

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == "/setup":
    #     return layout_setup_wizard
    if pathname == "/dashboard":
        return layout_dashboard
    else:
        return no_page

if __name__ == '__main__':
    hostname = "0.0.0.0"
    port = "80"

    app.run_server(
        port=port,
        debug=False,
        host=hostname,
        #dev_tools_ui=False,
        #dev_tools_props_check=False
    )