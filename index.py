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

import xmlrpc.client

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from .app import server
from .app import app
from .layouts import layout_info, layout_dashboard, no_page
from .callbacks import KoruzaGuiCallbacks
from .components.header import Header

from ..src.constants import KORUZA_MAIN_PORT

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
    Header(),
    html.Div(id='page-content')
])

# init client and pass it to callbacks
client = xmlrpc.client.ServerProxy(f"http://localhost:{KORUZA_MAIN_PORT}", allow_none=True)
KoruzaGuiCallbacks(client).callbacks()

# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == "/setup":
    #     return layout_setup_wizard
    if pathname == "/info":
        return layout_info
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
