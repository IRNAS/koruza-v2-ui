import random
import dash
import logging

from dash.dependencies import Input, Output, State
from app import app

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class KoruzaGuiCallbacks():
    def __init__(self):
        """
        Initialize KoruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """

        self.tcp_client = None
        self.num = 1
    
    def callbacks(self):
        """Defines all callbacks used in GUI"""


        #  master unit info update
        @app.callback(
            [
                Output("motor-coord-x-master", "children"),
                Output("motor-coord-y-master", "children"),
                Output("sfp-rx-power-master", "children"),
                Output("sfp-tx-power-master", "children"),
            ],
            [
                Input("n-intervals-update-master-info", "n_intervals")
            ]
        )
        def update_master_info(n_intervals):
            #print("hellp works")
            self.num += 1
            return str(self.num), "-600", "-700", "300"


        #  slave unit info update
        @app.callback(
            [
                #Output("motor-coord-x-slave", "children"),
                Output("motor-coord-y-slave", "children"),
                Output("sfp-rx-power-slave", "children"),
                Output("sfp-tx-power-slave", "children")
            ],
            [
                Input("n-intervals-update-slave-info", "n_intervals")
            ]
        )
        def update_info(n_intervals):
            #print("hellp works")
            return "-600", "-700", "300"


        #  button callbacks
        @app.callback(
            [
                #Output("motor-coord-x-slave", "children"),  # dummy div for outputs with no effect
                Output("hidden-div", "children")
            ],
            [
                # # test
                #  master unit values
                Input("motor-control-btn-up-master", "n_clicks"),
                Input("motor-control-btn-left-master", "n_clicks"),
                Input("motor-control-btn-down-master", "n_clicks"),
                Input("motor-control-btn-right-master", "n_clicks"),

                #  slave unit values
                Input("motor-control-btn-up-slave", "n_clicks"),
                Input("motor-control-btn-left-slave", "n_clicks"),
                Input("motor-control-btn-down-slave", "n_clicks"),
                Input("motor-control-btn-right-slave", "n_clicks")
            ]
        )
        def update_button_action(motor_up_m, motor_left_m, motor_down_m, motor_right_m, motor_up_s, motor_left_s, motor_down_s, motor_right_s):
            print("Motor up")
            #if motor_up_m:
            
            ctx = dash.callback_context
            print(ctx)
            if ctx.triggered and ctx.triggered[0]['value'] > 0:

                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]
                print(split)
                #logging.info(split)

            return [""]