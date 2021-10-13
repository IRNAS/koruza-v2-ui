import dash
import logging
import dash_auth  # provides HTTP Basic Authentication
import dash_bootstrap_components as dbc  # replace with statically served css

from .components.functions import get_valid_users

# application scope configs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=int(10))

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

VALID_USERNAME_PASSWORD_PAIRS = get_valid_users()

# https://dash.plotly.com/authentication
# configure Basic Auth
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server
app.config["suppress_callback_exceptions"] = True