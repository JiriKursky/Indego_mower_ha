#################################################################
# !!! Rename sensors in section Develop of indego according this:
BOZENA_MOWER_POSITION = "sensor.bozena_mower_position"
BOZENA_STATE_DETAIL = "sensor.bozena_mower_state_detail"
BOZENA_STATE = "sensor.bozena_mower_state"
# end of renaming
#################################################################

# These entities are defined after Home Assistant is started
# You can change friendly name before starting
# Mark auto_create is start of block used by app_system do not touch
# Values and attributes are stored in /custom_entities.json
# Changing values in this file have impact to entities
# app_system is reading that
# Values are stored excluding of sensor
# @auto_create
MOWER_MAP = "input_text.mower_map"  #  {"friendly_name": "Map"}
BOZENA_ZAKAZ_SEKANI = "input_boolean.bozena_zakaz_sekani"  # {"friendly_name": "Do not mow","icon":"mdi:close-octagon"}
MAP_0_X = "input_number.indego_0_x"  # {"unit_of_measurement": "px", "max": 2000}
MAP_0_Y = "input_number.indego_0_y"  # {"unit_of_measurement": "px", "max": 2000}
MAP_1_X = "input_number.indego_1_x"  # {"unit_of_measurement": "px", "max": 2000}
MAP_1_Y = "input_number.indego_1_y"  # {"unit_of_measurement": "px", "max": 2000}
BOZENA_STATE_INT = "sensor.bozena_stav"  # {"friendly_name": "State"}
BOZENA_DOMA = (
    "binary_sensor.bozena_doma"  # {"friendly_name": "Home", "icon": "mdi:robot-mower"}
)
MOWER_X = "input_number.bozena_x"  # {"unit_of_measurement": "px", "max": 2000}
MOWER_Y = "input_number.bozena_y"  # {"unit_of_measurement": "px", "max": 2000}
BOZENA_DOMU = "input_boolean.bozena_domu"  # {"friendly_name": "Home", "icon":"mdi:home-import-outline"}
BOZENA_SEKAT = (
    "input_boolean.bozena_sekat"  # {"friendly_name": "Mow", "icon": "mdi:robot-mower"}
)
BOZENA_UPDATE = (
    "input_boolean.bozena_update"  # {"friendly_name": "Update", "icon":"mdi:refresh"}
)
BOZENA_PAUZA = "input_boolean.bozena_pauza"  # {"friendly_name": "Pause"}
RATIO_X = "sensor.indego_ratio_x"  # {"friendly_name": "Ratio x"}
RATIO_Y = "sensor.indego_ratio_Y"  # {"friendly_name": "Ratio y"}
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
