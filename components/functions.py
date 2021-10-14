"""
Functions used in callbacks and layouts
"""
import json
from .rx_indicator import rx_indicator

SECRETS_FILENAME = "./koruza_v2/koruza_v2_ui/secrets.json"

def update_rx_power_bar(id, signal_str):
    class_name = ""
    if signal_str > -40:
        class_name = "signal-strength-1"
    if signal_str >= -38:
        class_name = "signal-strength-2"
    if signal_str >= -34:
        class_name = "signal-strength-3"
    if signal_str >= -30:
        class_name = "signal-strength-4"
    if signal_str >= -25:
        class_name = "signal-strength-5"
    if signal_str >= -20:
        class_name = "signal-strength-6"
    if signal_str >= -15:
        class_name = "signal-strength-7"
    if signal_str >= -10:
        class_name = "signal-strength-8"
    if signal_str >= -5:
        class_name = "signal-strength-9"

    return rx_indicator(id=f"rx-power-bar-{id}", class_name=class_name)

def generate_marker(pos_x, pos_y, SQUARE_SIZE):
    marker_lb_rt = {
        "type": "line",
        "x0": pos_x - (SQUARE_SIZE / 2),
        "y0": pos_y - (SQUARE_SIZE / 2),
        "x1": pos_x + (SQUARE_SIZE / 2),
        "y1": pos_y + (SQUARE_SIZE / 2),
        "line": {
            "color": "#ff0000",
            "opacity": "1.0"
        }
    }
    marker_lt_rb = {
        "type": "line",
        "x0": pos_x - (SQUARE_SIZE / 2),
        "y0": pos_y + (SQUARE_SIZE / 2),
        "x1": pos_x + (SQUARE_SIZE / 2),
        "y1": pos_y - (SQUARE_SIZE / 2),
        "line": {
            "color": "#ff0000",
            "opacity": "1.0"
        }
    }

    return marker_lb_rt, marker_lt_rb

def get_valid_users():
    """Load valid users from secrets file for basic authentication"""
    valid_user_pass_pairs = {}
    with open(SECRETS_FILENAME, "r") as file:
        secrets_json = json.load(file)
        for user in secrets_json["users"]:
            for username, password in user.items():
                valid_user_pass_pairs[username] = password

    return valid_user_pass_pairs