import time
import dash
import json
import math
import socket
import random
import logging
from random import randint
from threading import Lock

from dash.dependencies import Input, Output, State

from .app import app
from .components.functions import generate_marker, update_rx_power_bar

from ..src.constants import SQUARE_SIZE
from ..src.camera_util import get_camera_config, get_set_zoom, calculate_zoom_area_position, calculate_marker_pos
from ..koruza_v2_tracking.algorithms.spiral_align import SpiralAlign

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
LOCALHOST = s.getsockname()[0]
s.close()
PORT = 8080
VIDEO_STREAM_SRC = f"http://{LOCALHOST}:{PORT}/?action=stream"

class KoruzaGuiCallbacks():
    def __init__(self, client, mode):
        """
        Initialize koruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """
        self.koruza_client = client
        self.lock = Lock()

        # load calibration into local storage
        self.lock.acquire()
        self.curr_calib = self.koruza_client.get_calibration()["calibration"]
        self.calib = self.koruza_client.get_calibration()["calibration"]
        self.lock.release()

        self.lock.acquire()
        self.zoomed_in = self.koruza_client.get_zoom_data()
        self.lock.release()

        self.mode = mode
        if self.mode == "primary":
            self.alignment_alg = SpiralAlign()
        
    
    def init_info_layout_callbacks(self):
        """Defines callbacks used on link information page"""

        # draw on graph
        @app.callback(
            [
                Output("rx-power-graph-local", "figure"),
                Output("tx-power-local", "children"),
                Output("rx-power-local", "children")
            ],
            [
                Input("n-intervals-update-local-info", "n_intervals")
            ],
            [
                State("rx-power-graph-local", "figure")
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
                Output("rx-power-graph-remote", "figure"),
                Output("tx-power-remote", "children"),
                Output("rx-power-remote", "children")
            ],
            [
                Input("n-intervals-update-remote-info", "n_intervals")
            ],
            [
                State("rx-power-graph-remote", "figure")
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
                log.warning(f"Error getting secondary sfp data: {e}")
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
            [
                Output("confirm-restore-calibration-dialog", "displayed"),
                Output("confirm-update-unit-dialog", "displayed"),
                Output("update-status-dialog", "displayed"),
                Output("update-status-dialog", "message")
            ],
            [
                Input("btn-restore-calib", "n_clicks"),
                Input("confirm-restore-calibration-dialog", "submit_n_clicks"),
                Input("btn-update-unit", "n_clicks"),
                Input("confirm-update-unit-dialog", "submit_n_clicks")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_restore_calibration(btn_restore, dialog_restore, btn_update, dialog_update):
            """Defines callbacks used to restore calibration"""

            ctx = dash.callback_context
            display_restore_calib_dialog = False
            display_update_unit_dialog = False
            display_update_status_dialog = False
            message = ""

            if ctx.triggered:
                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "btn-restore-calib":
                    display_restore_calib_dialog = True
                    
                if prop_id == "confirm-restore-calibration-dialog":
                    self.lock.acquire()
                    self.koruza_client.restore_calibration()
                    self.lock.release()

                if prop_id == "btn-update-unit":
                    display_update_unit_dialog = True

                if prop_id == "confirm-update-unit-dialog":
                    self.lock.acquire()
                    ret, ver = self.koruza_client.update_unit()
                    self.lock.release()
                    display_update_status_dialog = True
                    if ret is True:
                        message = f"The unit is updating to version: {ver}. The unit will restart once the update is finished!"
                    if ret is False:
                        message = f"The unit is already at the latest version: {ver}!"

            
            return display_restore_calib_dialog, display_update_unit_dialog, display_update_status_dialog, message

    def init_calibration_callbacks(self):
        """Defines all callbacks used on unit calibration page"""
        # draw on graph
        @app.callback(
            [
                Output("camera-overlay", "figure"),
                Output("confirm-calibration-dialog", "displayed"),
                Output("calibration-stream-container", "src")
            ],
            [
                Input("camera-overlay", "clickData"),
                Input("confirm-calibration-dialog", "submit_n_clicks"),
                Input("camera-zoom-slider", "value"),
                Input("calibration-btn", "n_clicks"),
            ],
            [
                State("camera-overlay", "figure"),
                State("camera-zoom-slider", "value")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_calibration_position(click_data, confirm_calib, zoom_changed, calib_btn, fig, zoom_state):
            """Update calibration position and save somewhere globally. TODO: a file with global config"""
            # HELP:
            # https://dash.plotly.com/annotations
            # https://plotly.com/python/creating-and-updating-figures/

            ctx = dash.callback_context
            display_confirm_calib_dialog = False
            # js = ""
            img_src = f"{VIDEO_STREAM_SRC}?{time.time()}"

            if ctx.triggered:
                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                print(f"split: {split}")

                if prop_id == "calibration-btn":
                    display_confirm_calib_dialog = True
                    
                if prop_id == "camera-zoom-slider":
                    self.lock.acquire()
                    # get current camera configuration (position of top left corner and zoom)
                    cam_config = get_camera_config()

                    marker_x = self.curr_calib["offset_x"]
                    marker_y = self.curr_calib["offset_y"]
                    self.curr_calib["zoom_level"] = zoom_state

                    img_p = math.sqrt(1.0 / zoom_state)

                    # covert to global coordinates
                    global_marker_x = marker_x * cam_config["img_p"] + cam_config["x"] * 720
                    global_marker_y = (1.0 - cam_config["y"]) * 720.0 - (720 - marker_y) * cam_config["img_p"]
                    marker_x = round(global_marker_x)
                    marker_y = round(global_marker_y)

                    # get new position of top left zoom area based on calculation
                    x, y, clamped_x, clamped_y = calculate_zoom_area_position(marker_x, marker_y, img_p)
                    
                    if img_p != 1.0:
                        marker_x, marker_y = calculate_marker_pos(x, y, img_p)

                    self.curr_calib["offset_x"] = marker_x
                    self.curr_calib["offset_y"] = marker_y
                    self.koruza_client.update_camera_config(None, clamped_x, clamped_y, img_p)
                    line_lb_rt, line_lt_rb = generate_marker(marker_x, marker_y, SQUARE_SIZE)
                    fig["layout"]["shapes"] = [line_lb_rt, line_lt_rb]  # draw new shape
                    
                    self.lock.release()

                if prop_id == "camera-overlay":
                    try:
                        self.curr_calib["offset_x"] = click_data["points"][0]["x"]
                        self.curr_calib["offset_y"] = click_data["points"][0]["y"]
                        self.curr_calib["zoom_level"] = zoom_state

                        print(f"curr_calib: {self.curr_calib}")

                        line_lb_rt, line_lt_rb = generate_marker(self.curr_calib["offset_x"], self.curr_calib["offset_y"], SQUARE_SIZE)
                        fig["layout"]["shapes"] = [line_lb_rt, line_lt_rb]  # draw new shape
                    except Exception as e:
                        log.warning(f"An error occured when setting calibration: {e}")

                if prop_id == "confirm-calibration-dialog":
                    self.lock.acquire()
                    self.calib["offset_x"] = self.curr_calib["offset_x"]
                    self.calib["offset_y"] = self.curr_calib["offset_y"]
                    self.calib["zoom_level"] = self.curr_calib["zoom_level"]
                    

                    self.koruza_client.update_calibration(self.calib)
                    self.koruza_client.update_camera_calib()
                    self.lock.release()
            
            return fig, display_confirm_calib_dialog, img_src


    def init_dashboard_callbacks(self):
        """Defines all callbacks used on unit dashboard page"""

        # draw on graph
        @app.callback(
            [
                Output("video-stream-container", "src"),
                Output("calibration-img-container", "src")
            ],
            [
                Input("camera-zoom-toggle", "checked")
            ],
            [
                State("camera-zoom-toggle", "checked")
            ],
            prevent_initial_call=True  # TIL this is supposed to not trigger the initial
        )
        def update_calibration_position(zoom_checked, zoom_state):
            """Update calibration position and save somewhere globally. TODO: a file with global config"""
            # HELP:
            # https://dash.plotly.com/annotations
            # https://plotly.com/python/creating-and-updating-figures/

            ctx = dash.callback_context
            display_confirm_calib_dialog = False
            # js = ""
            img_src = f"{VIDEO_STREAM_SRC}?{time.time()}"

            if ctx.triggered:
                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "camera-zoom-toggle":
                    self.lock.acquire()
                    self.koruza_client.update_zoom_data(zoom_checked)
                    self.zoomed_in = zoom_checked
                    marker_x = self.calib["offset_x"]
                    marker_y = self.calib["offset_y"]
                    camera_config = self.koruza_client.get_camera_config()
                    if zoom_checked:
                        self.koruza_client.focus_on_marker(marker_x, marker_y, camera_config["IMG_P"], camera_config)
                    else:
                        self.koruza_client.update_camera_config(None, 0, 0, 1)  # default zoomed out settings
                    self.lock.release()
            
            return img_src, img_src

        #  local unit info update
        @app.callback(
            [
                Output("motor-coord-x-local", "children"),
                Output("motor-coord-y-local", "children"),
                Output("sfp-rx-power-local", "children"),
                Output("rx-bar-container-local", "children")
            ],
            [
                Input("n-intervals-update-local-info", "n_intervals")
            ]
        )
        def update_local_info(n_intervals):
            """
            Updates local unit info:
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

            rx_bar = update_rx_power_bar(id="primary", signal_str=rx_power_dBm)
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

        #  remote unit info update
        @app.callback(
            [
                Output("motor-coord-x-remote", "children"),
                Output("motor-coord-y-remote", "children"),
                Output("sfp-rx-power-remote", "children"),
                Output("rx-bar-container-remote", "children")
            ],
            [
                Input("n-intervals-update-remote-info", "n_intervals")
            ]
        )
        def update_remote_info(n_intervals):
            """
            Updates secondary unit info:
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
                log.warning(f"Error getting secondary sfp data: {e}")
            self.lock.release()
            # print(f"Duration of get_sfp_diagnostics on remote RPC call: {time.time() - start_time}")

            rx_power = 0
            rx_power_dBm = -40
            if sfp_data:
                rx_power = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power", 0)
                rx_power_dBm = sfp_data.get("sfp_0", {}).get("diagnostics", {}).get("rx_power_dBm", -40)
            
            rx_bar = update_rx_power_bar(id="secondary", signal_str=rx_power_dBm)
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

        # remote button callbacks
        @app.callback(
            Output("confirm-homing-dialog-remote", "displayed"),
            [
                Input("keyboard", "n_keydowns"),  # listen for keyboard input
                #  secondary unit values
                Input("motor-control-btn-up-remote", "n_clicks"),
                Input("motor-control-btn-left-remote", "n_clicks"),
                Input("motor-control-btn-down-remote", "n_clicks"),
                Input("motor-control-btn-right-remote", "n_clicks"),
                Input("motor-control-btn-center-remote", "n_clicks"),
                Input("led-slider-remote", "checked"),
                Input("confirm-homing-dialog-remote", "submit_n_clicks")
            ],
            [
                State("steps-dropdown-remote", "value"),
                State("keyboard", "keydown")
            ]
        )
        def update_remote_button_action(n_keydowns, motor_up, motor_left, motor_down, motor_right, motor_center, led_toggle, confirm_center, steps, event):

            display_remote_homing_dialog = False
            ctx = dash.callback_context
            
            if steps is None:
                steps = 0  # TODO handle elsewhere?

            if ctx.triggered:

                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "keyboard":
                    # secondary unit movement
                    if event["key"] == "ArrowUp":
                        log.info(f"move secondary up for {steps}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (0, steps, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowDown":
                        log.info(f"move secondary down for {steps}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (0, -steps, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowRight":
                        log.info(f"move secondary left for {steps}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (steps, 0, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "ArrowLeft":
                        log.info(f"move secondary right for {steps}")
                        self.lock.acquire()
                        try:
                            self.koruza_client.issue_remote_command("move_motors", (-steps, 0, 0))
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()

                #  remote unit callbacks
                if prop_id == "motor-control-btn-up-remote":
                    log.info(f"move secondary up {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, steps, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-remote":
                    log.info(f"move secondary down {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (0, -steps, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-remote":
                    log.info(f"move secondary left {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (-steps, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-remote":
                    log.info(f"move secondary right {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("move_motors", (steps, 0, 0))
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-remote":
                    log.info(f"confirm home secondary")
                    self.lock.acquire()
                    try:
                        self.koruza_client.issue_remote_command("home", ())
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-center-remote":
                    display_remote_homing_dialog = True

                if prop_id == "led-slider-remote":
                    self.lock.acquire()
                    # TODO implement synchronization of remote and local state of toggle
                    if led_toggle:
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

            return display_remote_homing_dialog

        # local button callbacks
        @app.callback(
            [
                Output("confirm-homing-dialog-local", "displayed"),
                Output("confirm-align-dialog-local", "displayed")
            ],
            [
                Input("keyboard", "n_keydowns"),  # listen for keyboard input

                #  primary unit values
                Input("motor-control-btn-up-local", "n_clicks"),
                Input("motor-control-btn-left-local", "n_clicks"),
                Input("motor-control-btn-down-local", "n_clicks"),
                Input("motor-control-btn-right-local", "n_clicks"),
                Input("motor-control-btn-center-local", "n_clicks"),
                Input("motor-control-btn-align-local", "n_clicks"),
                Input("led-slider-local", "checked"),
                Input("confirm-homing-dialog-local", "submit_n_clicks"),
                Input("confirm-align-dialog-local", "submit_n_clicks"),
            ],
            [
                State("steps-dropdown-local", "value"),
                State("keyboard", "keydown")
            ]
        )
        def update_button_action(n_keydowns, motor_up, motor_left, motor_down, motor_right, motor_home, align_units, led_toggle, confirm_center, confirm_align, steps, event):
            """
            Trigger button callbacks. On every click one of these callbacks is triggered.
            """
            display_local_homing_dialog = False
            display_local_align_dialog = False
            
            ctx = dash.callback_context
            
            if steps is None:
                steps = 0  # TODO handle elsewhere?

            if ctx.triggered:

                split = ctx.triggered[0]["prop_id"].split(".")
                prop_id = split[0]

                if prop_id == "keyboard":


                    # primary unit movement
                    if event["key"] == "w":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(0, steps, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "s":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(0, -steps, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "d":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(steps, 0, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()
                    if event["key"] == "a":
                        self.lock.acquire()
                        try:
                            self.koruza_client.move_motors(-steps, 0, 0)
                        except Exception as e:
                            log.warning(e)
                        self.lock.release()

                #  primary unit callbacks
                if prop_id == "motor-control-btn-up-local":
                    log.info(f"move primary up for {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, steps, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-down-local":
                    log.info(f"move primary down for {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(0, -steps, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-left-local":
                    log.info(f"move primary left for {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(-steps, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "motor-control-btn-right-local":
                    log.info(f"move primary right for {steps}")
                    self.lock.acquire()
                    try:
                        self.koruza_client.move_motors(steps, 0, 0)
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-homing-dialog-local":
                    log.info(f"confirm home primary")

                    self.lock.acquire()
                    try:
                        self.koruza_client.home()
                    except Exception as e:
                        log.warning(e)
                    self.lock.release()

                if prop_id == "confirm-align-dialog-local":
                    log.info(f"confirm align primary")

                    if self.mode == "primary":
                        self.alignment_alg.align_alternatingly()  # start spiral align

                if prop_id == "motor-control-btn-center-local":
                    display_local_homing_dialog = True

                if prop_id == "motor-control-btn-align-local":
                    display_local_align_dialog = True

                if prop_id == "led-slider-local":
                    # print("TOGGLING LED")
                    self.lock.acquire()
                    if led_toggle:
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
                
            return display_local_homing_dialog, display_local_align_dialog
