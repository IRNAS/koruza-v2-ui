import random
import dash
import logging
import json
import time
from random import randint
from threading import Lock

from dash.dependencies import Input, Output, State

from .app import app
from .components.functions import generate_marker, update_rx_power_bar

from ..src.constants import SQUARE_SIZE
from ..koruza_v2_tracking.algorithms.spiral_align import SpiralAlign

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class KoruzaGuiCallbacks():
    def __init__(self, client, mode):
        """
        Initialize koruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """
        self.koruza_client = client
        self.lock = Lock()

        self.mode = mode
        if self.mode == "primary":
            self.alignment_alg = SpiralAlign()
        
    
    def init_info_layout_callbacks(self):
        """Defines callbacks used on link information page"""

        # draw on graph
        @app.callback(
            [
                Output("rx-power-graph-primary", "figure"),
                Output("tx-power-primary", "children"),
                Output("rx-power-primary", "children")
            ],
            [
                Input("n-intervals-update-primary-info", "n_intervals")
            ],
            [
                State("rx-power-graph-primary", "figure")
            ]
        )
        def update_primary_information(n, rx_power_graph):
            # update sfp diagnostics
            sfp_data = {}
            self.lock.acquire()  # TODO maybe move locks to koruza.py?
            try:
                sfp_data = self.koruza_client.get_sfp_diagnostics()
                # print(sfp_data)
            except Exception as e:
                log.error(e)
            self.lock.release()

            rx_power = 0
            rx_power_dBm = -40
            tx_power = 0
            tx_power_dBm = -40
            if sfp_data:
                rx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power", 0)
                rx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)
                tx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power", 0)
                tx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)

            rx_dBm_list = rx_power_graph["data"][0]["y"]
            rx_dBm_list.append(rx_power_dBm)
            rx_dBm_list = rx_dBm_list[-100:]

            rx_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)
            tx_label = "{:.4f} mW ({:.3f} dBm)".format(tx_power, tx_power_dBm)

            rx_power_graph["data"][0]["y"] = rx_dBm_list
            rx_power_graph["data"][0]["x"] = [t for t in range(-len(rx_dBm_list), 0)]

            return rx_power_graph, tx_label, rx_label

        # draw on graph
        @app.callback(
            [
                Output("rx-power-graph-secondary", "figure"),
                Output("tx-power-secondary", "children"),
                Output("rx-power-secondary", "children")
            ],
            [
                Input("n-intervals-update-secondary-info", "n_intervals")
            ],
            [
                State("rx-power-graph-secondary", "figure")
            ]
        )
        def update_secondary_information(n, rx_power_graph):
            # update sfp diagnostics
            self.lock.acquire()  # will block until completed
            try:
                # print("Getting remote sfp diagnostics")
                sfp_data = self.koruza_client.issue_remote_command("get_sfp_diagnostics", ())
                # print(f"Gotten remote sfp diagnostics: {sfp_data}")
            except Exception as e:
                sfp_data = {}
                log.warning(f"Error getting slave sfp data: {e}")
            self.lock.release()

            rx_power = 0
            rx_power_dBm = -40
            tx_power = 0
            tx_power_dBm = -40

            if sfp_data:
                rx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power", 0)  # TODO: is this informative enough? if there is no sfp should no info be displayed?
                rx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)
                tx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("tx_power", 0)
                tx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)

            rx_dBm_list = rx_power_graph["data"][0]["y"]
            rx_dBm_list.append(rx_power_dBm)
            rx_dBm_list = rx_dBm_list[-100:]

            rx_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)
            tx_label = "{:.4f} mW ({:.3f} dBm)".format(tx_power, tx_power_dBm)

            rx_power_graph["data"][0]["y"] = rx_dBm_list
            rx_power_graph["data"][0]["x"] = [t for t in range(-len(rx_dBm_list), 0)]

            return rx_power_graph, tx_label, rx_label

        @app.callback(
            Output("confirm-restore-calibration-dialog", "displayed"),
            [
                Input("btn-restore-calib", "n_clicks"),
                Input("confirm-restore-calibration-dialog", "submit_n_clicks")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_restore_calibration(btn_restore, dialog_restore):
            """Defines callbacks used to restore calibration"""

            ctx = dash.callback_context
            display_restore_calib_dialog = False

            if ctx.triggered:
                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "btn-restore-calib":
                    display_restore_calib_dialog = True
                    
                if prop_id == "confirm-restore-calibration-dialog":
                    self.lock.acquire()
                    self.koruza_client.restore_calibration()
                    self.lock.release()
            
            return display_restore_calib_dialog


    def init_dashboard_callbacks(self):
        """Defines all callbacks used on unit dashboard page"""

        # draw on graph
        @app.callback(
            [
                Output("camera-overlay", "figure"),
                Output("confirm-calibration-dialog", "displayed")
            ],
            [
                Input("camera-overlay", "clickData"),
                Input("confirm-calibration-dialog", "submit_n_clicks")
            ],
            [
                State("camera-overlay", "figure")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_calibration_position(click_data, confirm_calib, fig):
            """Update calibration position and save somewhere globally. TODO: a file with global config"""
            # HELP:
            # https://dash.plotly.com/annotations
            # https://plotly.com/python/creating-and-updating-figures/

            ctx = dash.callback_context
            display_confirm_calib_dialog = False

            print(ctx.triggered)

            if ctx.triggered:
                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "camera-overlay":
    
                    try:
                        line_lb_rt, line_lt_rb = generate_marker(click_data["points"][0]["x"], click_data["points"][0]["y"], SQUARE_SIZE)

                        # TODO convert camera coordinates to motor coordinates
                        fig["layout"]["shapes"] = [line_lb_rt, line_lt_rb]  # draw new shape

                        self.calib = []
                        self.calib.append(("offset_x", click_data["points"][0]["x"]))
                        self.calib.append(("offset_y", click_data["points"][0]["y"]))

                        display_confirm_calib_dialog = True

                    except Exception as e:
                        log.warning(f"An error occured when setting calibration: {e}")
                    
                if prop_id == "confirm-calibration-dialog":
                    self.lock.acquire()
                    self.koruza_client.update_calibration(self.calib)
                    self.lock.release()
            
            return fig, display_confirm_calib_dialog

        #  master unit info update
        @app.callback(
            [
                Output("motor-coord-x-primary", "children"),
                Output("motor-coord-y-primary", "children"),
                Output("sfp-rx-power-primary", "children"),
                Output("rx-bar-container-primary", "children")
            ],
            [
                Input("n-intervals-update-primary-info", "n_intervals")
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
            sfp_data = {}
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
                rx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power", 0)
                rx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)

            rx_bar = update_rx_power_bar(id="master", signal_str=rx_power_dBm)
            rx_power_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)
            # print(rx_power_label)

            self.lock.acquire()
            # print(f"Acquiring motor position lock")
            try:
                # print("Getting local motors position")
                motor_x, motor_y = self.koruza_client.get_motors_position()
            except Exception as e:
                motor_x = 0
                motor_y = 0
            self.lock.release()
            # print(f"Releasing motor position lock")
                
            return motor_x, motor_y, rx_power_label, rx_bar

        #  slave unit info update
        @app.callback(
            [
                Output("motor-coord-x-secondary", "children"),
                Output("motor-coord-y-secondary", "children"),
                Output("sfp-rx-power-secondary", "children"),
                Output("rx-bar-container-secondary", "children")
            ],
            [
                Input("n-intervals-update-secondary-info", "n_intervals")
            ]
        )
        def update_slave_info(n_intervals):
            """
            Updates slave unit info:
                - RX
                - TX
                - LEDs
                
            Input: 
                n_intervals increment triggers this callback.
            """
            # update sfp diagnostics
            sfp_data = {}
            
            start_time = time.time()
            self.lock.acquire()  # will block until completed
            try:
                # print("Getting remote sfp diagnostics")
                sfp_data = self.koruza_client.issue_remote_command("get_sfp_diagnostics", ())
                # print(f"Gotten remote sfp diagnostics: {sfp_data}")
            except Exception as e:
                log.warning(f"Error getting slave sfp data: {e}")
            self.lock.release()
            # print(f"Duration of get_sfp_diagnostics on remote RPC call: {time.time() - start_time}")

            rx_power = 0
            rx_power_dBm = -40
            if sfp_data:
                rx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power", 0)
                rx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)
            
            rx_bar = update_rx_power_bar(id="slave", signal_str=rx_power_dBm)
            rx_power_label = "{:.4f} mW ({:.3f} dBm)".format(rx_power, rx_power_dBm)

            start_time = time.time()
            self.lock.acquire()
            try:
                # print("Getting remote motors position")
                motor_x, motor_y = self.koruza_client.issue_remote_command("get_motors_position", ())  # NOTE: works confirmed
                # print(f"Remote motor x: {motor_x}, remote motor y: {motor_y}")
            except Exception as e:
                motor_x = 0
                motor_y = 0
            self.lock.release()
            # print(f"Duration of get_motors_position on remote RPC call: {time.time() - start_time}")
                
            return motor_x, motor_y, rx_power_label, rx_bar

        #  button callbacks
        @app.callback(
            [
                Output("confirm-homing-dialog-primary", "displayed"),
                Output("confirm-homing-dialog-secondary", "displayed"),
                Output("confirm-align-dialog-primary", "displayed")
            ],
            [
                Input("keyboard", "n_keydowns"),  # listen for keyboard input

                #  master unit values
                Input("motor-control-btn-up-primary", "n_clicks"),
                Input("motor-control-btn-left-primary", "n_clicks"),
                Input("motor-control-btn-down-primary", "n_clicks"),
                Input("motor-control-btn-right-primary", "n_clicks"),
                Input("motor-control-btn-center-primary", "n_clicks"),
                Input("motor-control-btn-align-primary", "n_clicks"),
                Input("led-slider-primary", "checked"),
                Input("confirm-homing-dialog-primary", "submit_n_clicks"),
                Input("confirm-align-dialog-primary", "submit_n_clicks"),

                #  slave unit values
                Input("motor-control-btn-up-secondary", "n_clicks"),
                Input("motor-control-btn-left-secondary", "n_clicks"),
                Input("motor-control-btn-down-secondary", "n_clicks"),
                Input("motor-control-btn-right-secondary", "n_clicks"),
                Input("motor-control-btn-center-secondary", "n_clicks"),
                Input("led-slider-secondary", "checked"),
                Input("confirm-homing-dialog-secondary", "submit_n_clicks")
            ],
            [
                State("steps-dropdown-primary", "value"),
                State("steps-dropdown-secondary", "value"),
                State("keyboard", "keydown")
            ]
        )
        def update_button_action(n_keydowns, motor_up_m, motor_left_m, motor_down_m, motor_right_m, motor_center_m, units_align_m, led_toggle_m, confirm_center_m, confirm_align_m, motor_up_s, motor_left_s, motor_down_s, motor_right_s, motor_center_s, led_toggle_s, confirm_center_s, steps_m, steps_s, event):
            """
            Trigger button callbacks. On every click one of these callbacks is triggered.
            """
            display_master_homing_dialog = False
            display_slave_homing_dialog = False
            
            display_master_align_dialog = False
            
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
                if prop_id == "motor-control-btn-up-primary":
                    log.info(f"move master up for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, steps_m, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-primary":
                    log.info(f"move master down for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, -steps_m, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-primary":
                    log.info(f"move master left for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(-steps_m, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-primary":
                    log.info(f"move master right for {steps_m}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(steps_m, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-primary":
                    log.info(f"confirm home master")

                    self.lock.acquire()
                    try:
                        self.koruza_client.home()
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-align-dialog-primary":
                    log.info(f"confirm align master")

                    if self.mode == "primary":
                        self.alignment_alg.align_alternatingly()  # start spiral align

                if prop_id == "motor-control-btn-center-primary":
                    display_master_homing_dialog = True

                if prop_id == "motor-control-btn-align-primary":
                    display_master_align_dialog = True

                if prop_id == "led-slider-primary":
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
                if prop_id == "motor-control-btn-up-secondary":
                    log.info(f"move slave up {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, steps_s, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-secondary":
                    log.info(f"move slave down {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, -steps_s, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-secondary":
                    log.info(f"move slave left {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (-steps_s, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-secondary":
                    log.info(f"move slave right {steps_s}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (steps_s, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-secondary":
                    log.info(f"confirm home slave")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("home", ())
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-center-secondary":
                    display_slave_homing_dialog = True

                if prop_id == "led-slider-secondary":
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

            return display_master_homing_dialog, display_slave_homing_dialog, display_master_align_dialog
