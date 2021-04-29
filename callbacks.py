import random
import dash
import logging
import json
import time
from threading import Lock

from dash.dependencies import Input, Output, State

from .app import app
from .components.functions import generate_marker, update_rx_power_bar

from ..src.constants import SQUARE_SIZE

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class KoruzaGuiCallbacks():
    def __init__(self, client):
        """
        Initialize koruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """
        self.koruza_client = client
        self.lock = Lock()
    
    def callbacks(self):
        """Defines all callbacks used in GUI"""

        # draw on graph
        @app.callback(
            Output("camera-overlay", "figure"),
            [
                Input("camera-overlay", "clickData")
            ],
            [
                State("camera-overlay", "figure")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_calibration_position(click_data, fig):
            """Update calibration position and save somewhere globally. TODO: a file with global config"""
            # HELP:
            # https://dash.plotly.com/annotations
            # https://plotly.com/python/creating-and-updating-figures/
  
            try:
                line_lb_rt, line_lt_rb = generate_marker(click_data["points"][0]["x"], click_data["points"][0]["y"], SQUARE_SIZE)

                # TODO convert camera coordinates to motor coordinates
                fig["layout"]["shapes"] = [line_lb_rt, line_lt_rb]  # draw new shape

                key_data_pairs = []
                key_data_pairs.append(("offset_x", click_data["points"][0]["x"]))
                key_data_pairs.append(("offset_y", click_data["points"][0]["y"]))
                self.koruza_client.update_calibration_data(key_data_pairs)
            

            except Exception as e:
                log.warning(e)
            
            return fig

        #  master unit info update
        @app.callback(
            [
                Output("motor-coord-x-master", "children"),
                Output("motor-coord-y-master", "children"),
                Output("sfp-rx-power-master", "children"),
                Output("rx-bar-container-master", "children")
            ],
            [
                Input("n-intervals-update-master-info", "n_intervals")
            ]
        )
        def update_master_info(n_intervals):
            """
            Updates master unit info:
                - RX
                - TX
                - LEDs
                
            Input: 
                n_intervals increment triggers this callback.
            """
            
            # update sfp diagnostics
            sfp_data = None
            self.lock.acquire()  # TODO maybe move locks to koruza.py?
            try:
                sfp_data = self.koruza_client.get_sfp_diagnostics()
                # print(sfp_data)
            except Exception as e:
                log.error(e)
            self.lock.release()

            rx_power = 0
            rx_power_dBm = -40
            if sfp_data:
                rx_power = sfp_data["sfp_0"]["diagnostics"]["rx_power"]
                rx_power_dBm = sfp_data["sfp_0"]["diagnostics"]["rx_power_dBm"]

            rx_bar = update_rx_power_bar(id="master", signal_str=rx_power_dBm)
            rx_power_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)
            # print(rx_power_label)

            self.lock.acquire()
            try:
                # print("Getting local motors position")
                motor_x, motor_y = self.koruza_client.get_motors_position()
            except Exception as e:
                motor_x = 0
                motor_y = 0
            self.lock.release()
                
            return motor_x, motor_y, rx_power_label, rx_bar

        #  slave unit info update
        @app.callback(
            [
                Output("motor-coord-x-slave", "children"),
                Output("motor-coord-y-slave", "children"),
                Output("sfp-rx-power-slave", "children"),
                Output("rx-bar-container-slave", "children")
            ],
            [
                Input("n-intervals-update-slave-info", "n_intervals")
            ]
        )
        def update_slave_info(n_intervals):
            """
            PLACEHOLDER, WAITING FOR IMPLEMENTATION OF D2D MGMT.
            TODO: MOVE TO MAIN!!
           
             Updates slave unit info:
                - RX
                - TX
                - LEDs
                
            Input: 
                n_intervals increment triggers this callback.
            """
            # update sfp diagnostics
            self.lock.acquire()  # will block until completed
            try:
                # print("Getting remote sfp diagnostics")
                sfp_data = self.koruza_client.issue_remote_command("get_sfp_diagnostics", ())
                # print(f"Gotten remote sfp diagnostics: {sfp_data}")
            except Exception as e:
                sfp_data = None
                log.warning(f"Error getting slave sfp data: {e}")
            self.lock.release()

            rx_power = 0
            rx_power_dBm = -40
            if sfp_data:
                rx_power = sfp_data["sfp_0"]["diagnostics"]["rx_power"]
                rx_power_dBm = sfp_data["sfp_0"]["diagnostics"]["rx_power_dBm"]
            
            rx_bar = update_rx_power_bar(id="slave", signal_str=rx_power_dBm)
            rx_power_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)

            self.lock.acquire()
            try:
                # print("Getting remote motors position")
                motor_x, motor_y = self.koruza_client.issue_remote_command("get_motors_position", ())  # NOTE: works confirmed
                # print(f"Remote motor x: {motor_x}, remote motor y: {motor_y}")
            except Exception as e:
                motor_x = 0
                motor_y = 0
            self.lock.release()
                
            return motor_x, motor_y, rx_power_label, rx_bar

        #  button callbacks
        @app.callback(
            [
                Output("confirm-homing-dialog-master", "displayed"),
                Output("confirm-homing-dialog-slave", "displayed")
            ],
            [
                Input("keyboard", "n_keydowns"),  # listen for keyboard input

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
                State("steps-dropdown-slave", "value"),
                State("keyboard", "keydown")
            ]
        )
        def update_button_action(n_keydowns, motor_up_m, motor_left_m, motor_down_m, motor_right_m, motor_center_m, led_toggle_m, confirm_center_m, motor_up_s, motor_left_s, motor_down_s, motor_right_s, motor_center_s, led_toggle_s, confirm_center_s, steps_m, steps_s, event):
            """
            Trigger button callbacks. On every click one of these callbacks is triggered.
            """
            display_master_homing_dialog = False
            display_slave_homing_dialog = False
            
            ctx = dash.callback_context
            
            if steps_m is None:
                steps_m = 0  # TODO handle elsewhere?

            if ctx.triggered:

                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "keyboard":


                    # master unit movement
                    if event["key"] == "w":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(0, steps_m, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "s":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(0, -steps_m, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "d":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(steps_m, 0, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "a":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(-steps_m, 0, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()


                    # slave unit movement
                    if event["key"] == "ArrowUp":
                        log.info(f"move slave up for {steps_s}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (0, steps_s, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowDown":
                        log.info(f"move slave down for {steps_s}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (0, -steps_s, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowRight":
                        log.info(f"move slave left for {steps_s}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (steps_s, 0, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowLeft":
                        log.info(f"move slave right for {steps_s}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (-steps_s, 0, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()


                #  master unit callbacks
                if prop_id == "motor-control-btn-up-master":
                    log.info(f"move master up for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, steps_m, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-master":
                    log.info(f"move master down for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, -steps_m, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-master":
                    log.info(f"move master left for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(-steps_m, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-master":
                    log.info(f"move master right for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(steps_m, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-master":
                    log.info(f"confirm home master")

                    self.lock.acquire()
                    try:
                        self.koruza_client.home()
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-center-master":
                    display_master_homing_dialog = True

                if prop_id == "led-slider-master":
                    # print("TOGGLING LED")
                    self.lock.acquire()
                    if led_toggle_m:
                        try:
                            self.koruza_client.toggle_led()
                        except Exception as e:
                            log.warning(e)
                    else:
                        try:
                            self.koruza_client.toggle_led()
                        except Exception as e:
                            log.warning(e)
                    self.lock.release()
                

                #  slave unit callbacks
                if prop_id == "motor-control-btn-up-slave":
                    log.info(f"move slave up {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, steps_s, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-slave":
                    log.info(f"move slave down {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, -steps_s, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-slave":
                    log.info(f"move slave left {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (-steps_s, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-slave":
                    log.info(f"move slave right {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (steps_s, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-slave":
                    log.info(f"confirm home slave")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("home", ())
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-center-slave":
                    display_slave_homing_dialog = True

                if prop_id == "led-slider-slave":
                    self.lock.acquire()
                    # TODO implement synchronization of remote and local state of toggle
                    if led_toggle_s:
                        try:
                            self.koruza_client.issue_remote_command("toggle_led", ())
                        except Exception as e:
                            log.warning(e)
                    else:
                        try:
                            self.koruza_client.issue_remote_command("toggle_led", ())
                        except Exception as e:
                            log.warning(e)
                    self.lock.release()

            return display_master_homing_dialog, display_slave_homing_dialog
