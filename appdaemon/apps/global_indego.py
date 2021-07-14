#################################################################
#
MOWER_POSITION = "sensor.indego_912600505_mower_position"
MOWER_STATE_DETAIL = "sensor.indego_912600505_mower_state_detail"
MOWER_STATE = "sensor.indego_912600505_mower_state"
LAWN_MOWED = "sensor.indego_912600505_lawn_mowed"
MOWER_BATTERY="sensor.indego_912600505_battery_percentage"

MOWER_STATE_JS = "sensor.mower_state"
LAWN_MOWED_JS = "sensor.lawn_mowed"
MOWER_BATTERY_JS="sensor.indego_battery_percentage"
MOWER_POSITION_JS="sensor.indego_mower_position"
#
#################################################################

# These entities are defined after Home Assistant is started
# You can change friendly name before starting here in comment brackets
# Mark auto_create is start of block used by app_system do not touch
# Values and attributes are stored in /custom_entities.json
# Changing values in this file have impact to entities
# app_system is reading that
# Values are stored excluding of sensor

# @auto_create
MOWER_MAP = "input_text.mower_map"  #  {"friendly_name": "Map", "initial": "/local/indego_map.svg"}
BOZENA_ZAKAZ_SEKANI = "input_boolean.bozena_zakaz_sekani"  # {"friendly_name": "Do not mow","icon":"mdi:close-octagon"}
MAP_0_X = "input_number.indego_0_x"  # {"friendly_name": "Red X", unit_of_measurement": "px", "min": 0, "max": 2000,  "mode": "box"}
MAP_0_Y = "input_number.indego_0_y"  # {"friendly_name": "Red Y", "unit_of_measurement": "px", "min": 0,"max": 2000, "mode": "box"}
MAP_1_X = "input_number.indego_1_x"  # {"friendly_name": "Green X", "unit_of_measurement": "px", "min": 0,"max": 2000, "mode": "box"}
MAP_1_Y = "input_number.indego_1_y"  # {"friendly_name": "Green Y", "unit_of_measurement": "px", "min": 0,"max": 2000, "mode": "box"}
BOZENA_STATE_INT = "sensor.bozena_stav"  # {"friendly_name": "State"}
INDEGO_HOME = (
    "binary_sensor.bozena_doma"  # {"friendly_name": "Home", "icon": "mdi:robot-mower"}
)
MOWER_X = "input_number.bozena_x"  # {"unit_of_measurement": "px", "min": 0, "max": 2000, "mode": "box"}
MOWER_Y = "input_number.bozena_y"  # {"unit_of_measurement": "px", "min": 0, "max": 2000, "mode": "box"}
BOZENA_DOMU = "input_boolean.bozena_domu"  # {"friendly_name": "Domů", "icon":"mdi:home-import-outline"}
BOZENA_SEKAT = (
    "input_boolean.bozena_sekat"  # {"friendly_name": "Mow", "icon": "mdi:robot-mower"}
)
BOZENA_UPDATE = (
    "input_boolean.bozena_update"  # {"friendly_name": "Update", "icon":"mdi:refresh"}
)
BOZENA_PAUZA = "input_boolean.bozena_pauza"  # {"friendly_name": "Pause"}
RATIO_X = "sensor.indego_ratio_x"  # {"friendly_name": "Ratio x"}
RATIO_Y = "sensor.indego_ratio_y"  # {"friendly_name": "Ratio y"}
INDEGO_MODULE_OK = (
    "input_boolean.indego_module_ok"  # {"friendly_name": "Modules checked"}
)
SENSOR_INDEGO_MODULE = "sensor.indego_module"  # {"friendly_name": "Indego module"}
# @end

C_MOVING = "Mowing"

##########################################
# For English or you can put your language:
# TRANSLATE = {}
TRANSLATE = {
    C_MOVING: "Seká",
    "Docked": "Doma",
    "Border cut": "Seká okraj",
    "Sleeping": "Spí",
    "Mowing - Relocalising": "Hledá pozici",
    "Returning to dock - Lawn complete": "Návrat, hotovo",
    "Returning to dock - requested by user/app": "Příkaz návrat domů",
    "Charging": "Nabíjí se",
    "Paused": "Pauza",
}
