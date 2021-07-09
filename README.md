
# Indego Mower Map In Home Assistant 
[![GitHub release](https://img.shields.io/github/release/JiriKursky/Indego_mower_ha.svg)](https://github.com/JiriKursky/Indego_mower_ha/releases) 

Home Assistant Indego mower map. This is draft and if you have no experinces with AppDaemon 4 and button-card it can make you unhappy. You must have basic knowledge about configuration apps.yaml

However - it works. Tested on me and still working on that.

![Map example](/doc/m1-map.png)

Green and red points are for calibration, yellow is estimate position of Indego.
## Requirements
You need:

[AppDaemon 4](https://github.com/hassio-addons/addon-appdaemon) - you can install it as standard add-on via Supervisor

there is not necessary add in configuration of AppDaemon



[button-card](https://github.com/custom-cards/button-card) - you can install it from HACS

## Installation

1. In your directory /config/custom_components/ clone : https://github.com/JiriKursky/Indego. After restart of Home Assistant have to appear the new Indego sensor with position.

2. Rename sensors directly in Home Assistant UI according this file: https://github.com/JiriKursky/Indego_mower_ha/blob/main/appdaemon/apps/global_indego.py. You can also in this file switch off Czech language or put there your own.

3. You must have installation of AppFramework https://github.com/JiriKursky/AppFramework

4. Copy everything from this folder https://github.com/JiriKursky/Indego_mower_ha/blob/main/appdaemon/apps/ into your config/appdaemon/apps.This folder is automatically created after installing of add-on AppDaemon 4. Be aware if you have already apps.yaml in your folder - you should update it according that https://github.com/JiriKursky/Indego_mower_ha/blob/main/appdaemon/apps/apps.yaml 

## Next steps

5. If Indego component is working you should be able in Home Assistant to call service
![service](/doc/01-service.png)

No parameters. The service should create file config/www/indego_map.svg for using in lovelace.

Check AppDaemon Log - if there is an error maybe I omitted to export some library or restart AppDaemon.

Create new card in lovelace, add yaml and copy-paste there this [text](https://github.com/JiriKursky/Indego_mower_ha/blob/main/lovelace/indego_map_calibration.yaml)

You have to make calibration - describing will be later.

After calibration you can use this yaml https://github.com/JiriKursky/Indego_mower_ha/blob/main/lovelace/indego_map.yaml

I am sorry to use czech words inside code but I do not think that somebody will try this
