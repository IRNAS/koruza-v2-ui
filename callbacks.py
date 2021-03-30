import random
import dash
import logging
from threading import Lock

from dash.dependencies import Input, Output, State

from .app import app
from .components.functions import generate_rx_power_bar

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class KoruzaGuiCallbacks():
    def __init__(self, client):
        """
        Initialize koruzaGuiCallbacks class. Initializes tcp client used to send requests and listen for responses
        """
        self.koruza = client

        self.lock = Lock()

        self.rx_color_master = None
        self.master_led_on = False
    
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
            self.lock.acquire()  # will block until completed
            sfp_data = self.koruza.get_sfp_data()  # we probably need one for each sfp?
            self.lock.release()
            # print("Recv")
            # print(sfp_data["sfp_0"]["diagnostics"])
            # print("Trans")
            # print(sfp_data["sfp_1"]["diagnostics"])
            # self.sfp_wrapper.update_sfp_diagnostics()

            # rx_power = -3
            # rx_power = self.sfp_wrapper.get_module_diagnostics(SFP_RECEIVE)["rx_power"]
            rx_power = sfp_data["sfp_0"]["diagnostics"]["rx_power"]
            # rx_power = self.sfp_wrapper.get_module_diagnostics(SFP_TRANSMIT)["tx_power"]  # NOTE switched for visualization  - should be tx_power, but we're not displaying it
            # rx_power_dBm = self.sfp_wrapper.get_module_diagnostics(SFP_RECEIVE)["rx_power_dBm"]  # NOTE switched for visualization  - should be tx_power, but we're not displaying it
            rx_power_dBm = sfp_data["sfp_0"]["diagnostics"]["rx_power_dBm"]
            # rx_power_dBm = -30
            rx_value, rx_color = generate_rx_power_bar(rx_power_dBm)
            try:
                # motor_x = self.motor_wrapper.position_x
                # motor_y = self.motor_wrapper.position_y
                self.lock.acquire()
                motor_x, motor_y = self.koruza.get_motors_position()
                self.lock.release()
            except Exception as e:
                print(e)
                motor_x = 0
                motor_y = 0
            if self.master_led_on:
                # self.led_driver.set_color(rx_color, 0)
                self.lock.acquire()
                self.koruza.set_led_color(rx_color, 0)
                self.lock.release()

            
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
                Input("keyboard", "n_keydowns"),  # listen for keyboard input
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
                State("steps-dropdown-slave", "value"),
                State("keyboard", "keydown")
            ]
        )
        def update_button_action(n_keydowns, motor_up_m, motor_left_m, motor_down_m, motor_right_m, motor_center_m, led_toggle_m, confirm_center_m, motor_up_s, motor_left_s, motor_down_s, motor_right_s, motor_center_s, led_toggle_s, confirm_center_s, steps_m, steps_s, event):
            display_master_homing_dialog = False
            display_slave_homing_dialog = False
            
            ctx = dash.callback_context
            
            if steps_m is None:
                steps_m = 0  # TODO handle elsewhere?

            if ctx.triggered:

                split = ctx.triggered[0]["prop_id"].split(".")
                #print(split)
                prop_id = split[0]

                if prop_id == "keyboard":
                    #print(event)  # triggered event

                    # master unit movement
                    if event["key"] == "w":
                        # self.motor_wrapper.move_motor(0, steps_m, 0)
                        self.lock.acquire()
                        self.koruza.move_motors(0, steps_m, 0)
                        self.lock.release()
                    if event["key"] == "s":
                        # self.motor_wrapper.move_motor(0, -steps_m, 0)
                        self.lock.acquire()
                        self.koruza.move_motors(0, -steps_m, 0)
                        self.lock.release()
                    if event["key"] == "d":
                        # self.motor_wrapper.move_motor(steps_m, 0, 0)
                        self.lock.acquire()
                        self.koruza.move_motors(steps_m, 0, 0)
                        self.lock.release()
                    if event["key"] == "a":
                        # self.motor_wrapper.move_motor(-steps_m, 0, 0)
                        self.lock.acquire()
                        self.koruza.move_motors(-steps_m, 0, 0)
                        self.lock.release()

                    # slave unit movement
                    if event["key"] == "ArrowUp":
                        print(f"move master up for {steps_m}")
                    if event["key"] == "ArrowDown":
                        print(f"move master down for {steps_m}")
                    if event["key"] == "ArrowRight":
                        print(f"move master left for {steps_m}")
                    if event["key"] == "ArrowLeft":
                        print(f"move master right for {steps_m}")
                #print(prop_id)
                #  master unit callbacks
                if prop_id == "motor-control-btn-up-master":
                    print(f"move master up for {steps_m}")
                    # self.motor_wrapper.move_motor(0, steps_m, 0)
                    self.lock.acquire()
                    self.koruza.move_motors(0, steps_m, 0)
                    self.lock.release()
                if prop_id == "motor-control-btn-down-master":
                    print(f"move master down for {steps_m}")
                    # self.motor_wrapper.move_motor(0, -steps_m, 0)
                    self.lock.acquire()
                    self.koruza.move_motors(0, -steps_m, 0)
                    self.lock.release()
                if prop_id == "motor-control-btn-left-master":
                    print(f"move master left for {steps_m}")
                    # self.motor_wrapper.move_motor(steps_m, 0, 0)
                    self.lock.acquire()
                    self.koruza.move_motors(-steps_m, 0, 0)
                    self.lock.release()
                if prop_id == "motor-control-btn-right-master":
                    print(f"move master right for {steps_m}")
                    # self.motor_wrapper.move_motor(-steps_m, 0, 0)
                    self.lock.acquire()
                    self.koruza.move_motors(steps_m, 0, 0)
                    self.lock.release()
                if prop_id == "confirm-homing-dialog-master":
                    print(f"confirm home master")
                    # self.motor_wrapper.home()
                    self.lock.acquire()
                    self.koruza.home()
                    self.lock.release()
                if prop_id == "motor-control-btn-center-master":
                    display_master_homing_dialog = True
                if prop_id == "led-slider-master":
                    if led_toggle_m:
                        self.master_led_on = True
                        # self.led_driver.set_color("blue", 105)
                    else:
                        # self.led_driver.turn_off()
                        self.lock.acquire()
                        self.koruza.disable_led()
                        self.lock.release()
                        self.master_led_on = False
                

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