# KORUZA v2 Pro Graphical User Interface

## Description
The KORUZA v2 Pro Graphical User Interface enables monitoring and control of KORUZA v2 Pro units. The Graphical User Interface is written in Python with the help of Dash. 

## File Structure

Included code is structured following the guidelines provided by [dash](https://dash.plotly.com/urls).
* assets - icons, css styles and favicon
* components - custom components used in defined layouts
* layouts - layouts defining each page structure

```
.
|--- assets/
    |---icons
        |---.... icon images
    |---base-styles.css
    |---custom-styles.css
    |---favicon.ico
    
|--- components/
    |---camera_display.py
    |---control_button.py
    |---control_panel.py
    |---custom_toggle.py
    |---footer.py
    |---functions.py
    |---header.py
    |---rx_indicator.py
    |---rx_power_graph.py
    |---unit_control.py
    |---unit_info_panel.py

|--- layouts/
    |---dashboard_layout.py
    |---info_layout.py
    |---landing_page_layout.py
    
|---.gitignore
|---app.py
|---callbacks.py
|---index.py
|---LICENSE
|---README.md
|---requirements.txt

```


## License

Firmware and software originating from KORUZA v2 Pro project, including KORUZA v2 Pro UI, is licensed under [GNU General Public License v3.0](https://github.com/IRNAS/koruza-v2-ui/blob/main/LICENSE).

Open-source licensing means the hardware, firmware, software and documentation may be used without paying a royalty, and knowing one will be able to use their version forever. One is also free to make changes, but if one shares these changes, they have to do so under the same conditions they are using themselves. KORUZA, KORUZA v2 Pro and IRNAS are all names and marks of IRNAS LTD. These names and terms may only be used to attribute the appropriate entity as required by the Open Licence referred to above. The names and marks may not be used in any other way, and in particular may not be used to imply endorsement or authorization of any hardware one is designing, making or selling.

## Dependencies and older versions

* [KORUZA UI](https://github.com/IRNAS/koruza-ui) - Previous version of the Graphical User Interface for KORUZA Pro units.
