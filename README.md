# KORUZA Graphical User Interface

Introduction...

## Repository Structure

### Branches

| Branch | Description |
| ------ | ----------- |
| master | ... |

### File Structure
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
    |---no_page_layout.py
    
|---.gitignore
|---app.py
|---callbacks.py
|---index.py
|---LICENSE
|---README.md
|---requirements.txt

```


## License

All KORUZA software is published under [GNU General Public License v3.0](https://github.com/IRNAS/koruza-v2-ui/blob/main/LICENSE).

## Contribution
