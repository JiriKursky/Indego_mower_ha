# 1 Rename sensors of indego according this:
BOZENA_MOWER_POSITION = "sensor.bozena_mower_position"
BOZENA_STATE_DETAIL = "sensor.bozena_mower_state_detail"
BOZENA_STATE = "sensor.bozena_mower_state"
# end of renaming

# 2 Define these via HA helper
MOWER_MAP = "input_text.mower_map"
MOWER_X = "input_number.bozena_x"
MOWER_Y = "input_number.bozena_y"


MAP_0_X = "input_number.indego_0_x"
MAP_0_Y = "input_number.indego_0_y"
MAP_1_X = "input_number.indego_1_x"
MAP_1_Y = "input_number.indego_1_y"

BOZENA_DOMU = "input_boolean.bozena_domu"
BOZENA_SEKAT = "input_boolean.bozena_sekat"
BOZENA_PAUZA = "input_boolean.bozena_pauza"
BOZENA_ZAKAZ_SEKANI = "input_boolean.bozena_zakaz_sekani"
BOZENA_UPDATE = "input_boolean.bozena_update"
BOZENA_DEBUG = "input_boolean.bozena_debug"
# end of definig helpers

# For these leave it as it is

BOZENA_STATE_CZ = "sensor.bozena_stav"
BOZENA_DOMA = "binary_sensor.bozena_doma"
