
def generate_rx_power_bar(signal_str):
    color = ""
    value = -31
    if signal_str < -30:
        color = "#eb4034"
        value = 9
    elif signal_str <= -27:
        color = "#eb4f34"
        value = 18
    elif signal_str <= -24:
        color = "#eb5f34"
        value = 27
    elif signal_str <= -21:
        color = "#eb7734"
        value = 36
    elif signal_str <= -18:
        color = "#eb9934"
        value = 45
    elif signal_str <= -15:
        color = "#ebba34"
        value = 54
    elif signal_str <= -13:
        color = "#ebeb34"
        value = 63
    elif signal_str <= -10:
        color = "#d3eb34"
        value = 72
    elif signal_str <= -7:
        color = "#b7eb34"
        value = 81
    elif signal_str <= -4:
        color = "#34eb34"
        value = 90
    elif signal_str <= -1:
        color = "#34eb4c"
        value = 100

    return value, color