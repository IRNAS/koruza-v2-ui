
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