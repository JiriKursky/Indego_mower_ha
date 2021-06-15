# Indego Mower Home Assistant display
Home Assistant Indego mower map. This is draft and if you have no experinces with AppDaemon 4 and button-card it can make you unhappy. However - it works. Tested on me and still working on that.

![Map example](/doc/m1-map.png)

Green and red points are for calibration, yellow is estimate position of Indego.
## Requirements
You need:

[AppDaemon 4](https://github.com/hassio-addons/addon-appdaemon) - you can install it as standard add-on via Supervisor

[button-card](https://github.com/custom-cards/button-card) - you can install it from HACS



## Installation

You must have installed custom_component from here: https://github.com/JiriKursky/Indego

Copy appdaemon/apps into your folder config/appdaemon/apps. This folder is automatically created after installing of add-on

If Indego component is working you should be able in Home Assistant to call service
![service](/doc/01-service.png)

No parameters. The service should create in your config/www/indego_map.svg for using in lovelace.