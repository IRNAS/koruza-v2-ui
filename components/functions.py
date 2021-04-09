
def generate_rx_power_bar(signal_str):
    color = ""
    value = 2
    if signal_str >= -40:
        color = "#ff0000"
        value = 2
    if signal_str >= -38:
        color = "#ff4500"
        value = 14
    if signal_str >= -30:
        color = "#ff7f50"
        value = 28
    if signal_str >= -25:
        color = "#ff00ff"
        value = 42
    if signal_str >= -20:
        color = "#0000ff"
        value = 56
    if signal_str >= -15:
        color = "#0045ff"
        value = 70
    if signal_str >= -10:
        color = "#00ffff"
        value = 85
    if signal_str >= -5:
        color = "#00ff00"
        value = 100
  

    return value, color

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