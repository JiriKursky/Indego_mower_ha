# Indego Mower Home Assistant display
Home Assistant Indego mower map. This is draft and if you have no experinces with AppDaemon 4 and button-card it can make you unhappy. You must have basic knowledge about configuration apps.yaml

However - it works. Tested on me and still working on that.

![Map example](/doc/m1-map.png)

Green and red points are for calibration, yellow is estimate position of Indego.
## Requirements
You need:

[AppDaemon 4](https://github.com/hassio-addons/addon-appdaemon) - you can install it as standard add-on via Supervisor

[button-card](https://github.com/custom-cards/button-card) - you can install it from HACS



## Installation

1. You must installed custom_component from here: https://github.com/JiriKursky/Indego and see the new sensor with position.

2. Rename sensors directly in Home Assistant UI according this file 


If Indego component is working you should be able in Home Assistant to call service
![service](/doc/01-service.png)

No parameters. The service should create in your config/www/indego_map.svg for using in lovelace.

If map is generated you have to create following helpers:
|Name                         |Description                                    |Put manually |
|-----------------------------|-----------------------------------------------|-------------|
| `input_text.mower_map`      | /local/indego_map.svg                         |     yes     |
| `input_number.bozena_x`     | x-position in px on picture                   |             |
| `input_number.bozena_y`     | y position in px on picture                   |             | 
| `input_number.indego_0_x`   | x position for calibration left corner down   |     yes     |
| `input_number.indego_0_y`   | y position for calibration left corner down   |     yes     |
| `input_number.indego_1_x`   | x position for calibration right corner top   |     yes     |
| `input_number.indego_1_y`   | y position for calibration right corner top   |     yes     |

values you will put there later via lovelace card

Copy appdaemon/apps into your folder config/appdaemon/apps. This folder is automatically created after installing of add-on


Check AppDaemon Log - if there is an error maybe I omitted to export some library

custom-button must me installed

Create new card in lovelace, add yaml and copy-paste there this [text](https://github.com/JiriKursky/Indego_mower_ha/blob/main/lovelace/bozena_mapa.yaml)

