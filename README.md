
# Indego Mower Map In Home Assistant 
[![GitHub release](https://img.shields.io/github/release/JiriKursky/Indego_mower_ha.svg)](https://github.com/JiriKursky/Indego_mower_ha/releases) 


The original component was created by https://github.com/jm-73/Indego
Tested only with Indego S+ 350
I only add sensor and service


I am working on tutorial how to use that with AppDeamon.



![Map example](/doc/m1-map.png)

Yellow point is estimate position of Indego.

## Installation

1. In your directory /config/custom_components/ clone : https://github.com/JiriKursky/Indego. After restart of Home Assistant have to appear the new Indego sensor with position.

2. You must have installation of AppFramework https://appframework.readthedocs.io/en/latest/


## Next steps

If Indego component is working you should be able in Home Assistant to call service
![service](/doc/01-service.png)

No parameters. The service should create file /config/www/indego_map.svg for using in lovelace.
