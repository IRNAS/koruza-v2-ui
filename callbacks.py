import random
import dash
import logging

from dash.dependencies import Input, Output, State

from .app import app
from .components.functions import generate_rx_power_bar

from ..koruza_v2_driver.src.constants import SFP_TRANSMIT, SFP_RECEIVE  # TODO move

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class KoruzaGuiCallbacks():
    def __init__(self, motor_wrapper, led_driver, sfp_wrapper):
        """
        Initialize KoruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """

        self.tcp_client = None

        self.motor_wrapper = motor_wrapper
        self.led_driver = led_driver
        self.sfp_wrapper = sfp_wrapper
    
    def callbacks(self):
        """Defines all callbacks used in GUI"""


        #  master unit info update
        @app.callback(
            [
                Output("motor-coord-x-master", "children"),
                Output("motor-coord-y-master", "children"),
                Output("sfp-rx-power-master", "children"),
                #Output("sfp-tx-power-master", "children"),
                Output("rx-power-bar-master", "value"),
                Output("rx-power-bar-master", "color")
            ],
            [
                Input("n-intervals-update-master-info", "n_intervals")
            ]
        )
        def update_master_info(n_intervals):
            #print("hellp works")
            # update sfp diagnostics
            self.sfp_wrapper.update_sfp_diagnostics()

            # rx_power = -3
            rx_power = self.sfp_wrapper.get_module_diagnostics(SFP_RECEIVE)["rx_power"]
            rx_power = self.sfp_wrapper.get_module_diagnostics(SFP_TRANSMIT)["tx_power"]  # NOTE switched for visualization  - should be tx_power, but we're not displaying it
            rx_power_dBm = self.sfp_wrapper.get_module_diagnostics(SFP_TRANSMIT)["tx_power_dBm"]  # NOTE switched for visualization  - should be tx_power, but we're not displaying it
            rx_value, rx_color = generate_rx_power_bar(rx_power_dBm)
            motor_x = self.motor_wrapper.position_x
            motor_y = self.motor_wrapper.position_y
            return motor_x, motor_y, str(rx_power) + " (" + str(rx_power_dBm) + " dBm)", rx_value, rx_color


        # #  slave unit info update
        # @app.callback(
        #     [
        #         Output("motor-coord-x-slave", "children"),
        #         Output("motor-coord-y-slave", "children"),
        #         Output("sfp-rx-power-slave", "children"),
        #         #Output("sfp-tx-power-slave", "children"),
        #         Output("rx-power-bar-slave", "value"),
        #         Output("rx-power-bar-slave", "color")
        #     ],
        #     [
        #         Input("n-intervals-update-slave-info", "n_intervals")
        #     ]
        # )
        # def update_info(n_intervals):
        #     #print("hellp works")
        #     rx_power = -3
        #     rx_value, rx_color = generate_rx_power_bar(rx_power)
        #     return "500", "-600", str(rx_power) + "dB", rx_value, rx_color


        #  button callbacks
        @app.callback(
            [
                #Output("motor-coord-x-slave", "children"),  # dummy div for outputs with no effect
                Output("hidden-div", "children"),
                Output("confirm-homing-dialog-master", "displayed"),
                Output("confirm-homing-dialog-slave", "displayed")
            ],
            [
                # # test
                #  master unit values
                Input("motor-control-btn-up-master", "n_clicks"),
                Input("motor-control-btn-left-master", "n_clicks"),
                Input("motor-control-btn-down-master", "n_clicks"),
                Input("motor-control-btn-right-master", "n_clicks"),
                Input("motor-control-btn-center-master", "n_clicks"),
                Input("led-slider-master", "checked"),
                Input("confirm-homing-dialog-master", "submit_n_clicks"),

                #  slave unit values
                Input("motor-control-btn-up-slave", "n_clicks"),
                Input("motor-control-btn-left-slave", "n_clicks"),
                Input("motor-control-btn-down-slave", "n_clicks"),
                Input("motor-control-btn-right-slave", "n_clicks"),
                Input("motor-control-btn-center-slave", "n_clicks"),
                Input("led-slider-slave", "checked"),
                Input("confirm-homing-dialog-slave", "submit_n_clicks")
            ],
            [
                State("steps-dropdown-master", "value"),
                State("steps-dropdown-slave", "value")
            ]
        )
        def update_button_action(motor_up_m, motor_left_m, motor_down_m, motor_right_m, motor_center_m, led_toggle_m, confirm_center_m, motor_up_s, motor_left_s, motor_down_s, motor_right_s, motor_center_s, led_toggle_s, confirm_center_s, steps_m, steps_s):
            display_master_homing_dialog = False
            display_slave_homing_dialog = False
            
            ctx = dash.callback_context

            if steps_m is None:
                steps_m = 0  # TODO handle elsewhere

            if ctx.triggered:

                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]
                #print(prop_id)
                #  master unit callbacks
                if prop_id == "motor-control-btn-up-master":
                    print(f"move master up for {steps_m}")
                    self.motor_wrapper.move_motor(0, -steps_m, 0)
                if prop_id == "motor-control-btn-down-master":
                    print(f"move master down for {steps_m}")
                    self.motor_wrapper.move_motor(0, steps_m, 0)
                if prop_id == "motor-control-btn-left-master":
                    print(f"move master left for {steps_m}")
                    self.motor_wrapper.move_motor(-steps_m, 0, 0)
                if prop_id == "motor-control-btn-right-master":
                    print(f"move master right for {steps_m}")
                    self.motor_wrapper.move_motor(steps_m, 0, 0)
                if prop_id == "confirm-homing-dialog-master":
                    print(f"confirm home master")
                    self.motor_wrapper.home()
                if prop_id == "motor-control-btn-center-master":
                    display_master_homing_dialog = True
                if prop_id == "led-slider-master":
                    if led_toggle_m:
                        self.led_driver.set_color("blue", 105)
                    else:
                        self.led_driver.turn_off()
                

                #  slave unit callbacks
                if prop_id == "motor-control-btn-up-slave":
                    print(f"move slave up {steps_s}")
                if prop_id == "motor-control-btn-down-slave":
                    print(f"move slave down {steps_s}")
                if prop_id == "motor-control-btn-left-slave":
                    print(f"move slave left {steps_s}")
                if prop_id == "motor-control-btn-right-slave":
                    print(f"move slave right {steps_s}")
                if prop_id == "confirm-homing-dialog-slave":
                    print(f"confirm home slave {steps_s}")
                if prop_id == "motor-control-btn-center-slave":
                    display_slave_homing_dialog = True

            return None, display_master_homing_dialog, display_slave_homing_dialog