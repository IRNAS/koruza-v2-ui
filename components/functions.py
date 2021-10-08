"""
Functions used in callbacks and layouts
"""

from .rx_indicator import rx_indicator

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

def calculate_zoom_area_position(marker_x, marker_y, img_p):
    """Get zoom area upper left corner from marker position"""
    # print(f"Marker x: {marker_x}")
    # print(f"Marker y: {marker_y}")
    x = marker_x / 720 - img_p / 2  # default zoom level is 0.5
    y = 1.0 - (marker_y / 720) - img_p / 2
    # print(f"New x pos: {x}")
    # print(f"New y pos: {y}")

    return x, y, clamp(x, 0.0, 0.5), clamp(y, 0.0, 0.5)

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

def calculate_marker_pos(x, y, img_p):
    # move marker if zoomed in image is outside of bounds
    if x < 0:
        marker_x = 360.0 + ((1 / img_p) * x * 720.0)
    elif x > 0.5:
        marker_x = 360.0 + ((1 / img_p) * (x - 0.5)) * 720.0
    else:
        marker_x = 360.0
    
    if y < 0:
        marker_y = 360.0 - ((1 / img_p) * y * 720.0)
    elif y > 0.5:
        marker_y = 360.0 - ((1 / img_p) * (y - 0.5)) * 720.0
    else:
        marker_y = 360.0

    return marker_x, marker_y