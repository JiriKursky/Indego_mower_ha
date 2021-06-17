##############################################
# !!! Rename sensors of indego according this:
BOZENA_MOWER_POSITION = "sensor.bozena_mower_position"
BOZENA_STATE_DETAIL = "sensor.bozena_mower_state_detail"
BOZENA_STATE = "sensor.bozena_mower_state"
# end of renaming
############################################

# These leave them as it is
# define helpers
MOWER_MAP = "input_text.mower_map"
BOZENA_ZAKAZ_SEKANI = "input_boolean.bozena_zakaz_sekani"
MAP_0_X = "input_number.indego_0_x"
MAP_0_Y = "input_number.indego_0_y"
MAP_1_X = "input_number.indego_1_x"
MAP_1_Y = "input_number.indego_1_y"
BOZENA_STATE_INT = "sensor.bozena_stav"
BOZENA_DOMA = "binary_sensor.bozena_doma"
MOWER_X = "input_number.bozena_x"
MOWER_Y = "input_number.bozena_y"
BOZENA_DOMU = "input_boolean.bozena_domu"
BOZENA_SEKAT = "input_boolean.bozena_sekat"
BOZENA_UPDATE = "input_boolean.bozena_update"
BOZENA_PAUZA = "input_boolean.bozena_pauza"

DEF_ENTITIES = (
    (BOZENA_ZAKAZ_SEKANI, "Do not mow"),
    (MOWER_MAP, "Map"),
    (BOZENA_DOMU, "Home"),
    (BOZENA_PAUZA, "Pause"),
    (BOZENA_SEKAT, "Mow"),
    (BOZENA_UPDATE, "Update"),
    (BOZENA_STATE_INT, "State"),
    (BOZENA_DOMA, "Home"),
)
ENTITIES_PX = (MAP_0_X, MAP_0_Y, MAP_1_X, MAP_1_Y, MOWER_X, MOWER_Y)

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
