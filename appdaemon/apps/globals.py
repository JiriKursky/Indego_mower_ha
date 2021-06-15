POPLACH = "input_boolean.poplach"
POPLACH_GARAZ = "input_boolean.poplach_garaz"
POPLACH_DOMEK_NARADI = "input_boolean.poplach_naradi"
POPLACH_SKLENIK = "input_boolean.poplach_sklenik"


# Sonoff pouze pro čtení stavu - řídí pak přes fibaro


SWITCH_CHODBA = "switch.chodba"

SWITCH_ZASUVKA_KOTEL_RELE = "switch.zasuvka_kotel_rele"

SENSOR_CHODBA_U_PREDSINE = "binary_sensor.chodba_u_vchodu_37"
SENSOR_CHODBA_PREDNI = "binary_sensor.chodba_predni_31"
SENSOR_LUX_PREDSIN = "sensor.predsin_lux_61"
SENSOR_SPAJZ = "binary_sensor.spajz"
SENSOR_OKNO_LOZNICE = "binary_sensor.loznice_okno_27"
SENSOR_DOMEK_NARADI = "binary_sensor.domek_naradi"
SENSOR_VENKOVNI_TEPLOTA = "sensor.dark_sky_temperature"


KLIMA_CHLAZENI = "input_boolean.klima_chlazeni"


GOOGLE_OZNAMOVAT = "input_boolean.google_oznamovat"
GOOGLE_ZVONEK = "input_boolean.google_zvonek"  # Oznamit pomoci google, že někdo zvoní

PERSON_TATA = "person.tata"
PERSON_MAMA = "person.mama"
PERSON_STEPAN = "person.stepan"
PERSON_VASEK = "person.vasek"
PERSON_PETA = "person.peta"
OVLADANI_SKLENIK_A = "input_boolean.sklenik_a"

SWITCH_BABICKA_TEPLICE = "input_boolean.babicka_teplice"
SWITCH_BAZEN_SVETLO = "switch.bazen_svetlo"
SWITCH_SPAJZ = "switch.fibaro_system_fgs223_double_relay_switch_2"
SWITCH_GARAZ_ZASUVKA_TOPENI = "switch.garaz_topeni"

SWITCH_RAID = "switch.fibaro_system_fgwpe_f_wall_plug_gen5_switch_3"
SWITCH_STEPAN_RAID = "switch.stepan_raid"
SWITCH_TELEVIZE = "switch.televize"
SWITCH_SUBWOOFER = "switch.subwoofer"


NOCNI_REZIM = "input_boolean.nocni_rezim"
TIMER_NOCNI_REZIM = "input_boolean.nocni_rezim_timer"


INFORMOVAT = "input_boolean.informovat"


SWITCH_RESIDENTS_AUTOMAT = "input_boolean.residents_automat"
SWITCH_TOPENI_HA = "input_boolean.topeni_ha"
SWITCH_SUPER_NOC = "input_boolean.super_noc"


ZVONEK_VASEK = "switch.vasek_zvonek"
ZVONEK_PETA = "switch.peta_zvonek"
ZVONEK_STEPAN = "switch.stepan_zvonek"
ZVONEK_PREDSIN = "switch.zvonek"


RESTART_HA = "input_boolean.restart_ha"

ZABEZPECIT = "input_boolean.zabezpecit"
ZABEZPECIT_NARADI = "input_boolean.zabezpecit_naradi"
ZABEZPECIT_GARAZ = "input_boolean.zabezpecit_garaz"
ZABEZPECIT_SKLENIK = "input_boolean.zabezpecit_sklenik"

SENSOR_SKLENIK_1 = "binary_sensor.sklenik_dvere_1"
SWITCH_ZVONEK_VAROVANI = "switch.zvonek_varovani"

NOC_TURN_OFF = [
    SWITCH_CHODBA,
    SWITCH_SPAJZ,
    SWITCH_GARAZ_ZASUVKA_TOPENI,
    SWITCH_TELEVIZE,
    SWITCH_SUBWOOFER,
    SWITCH_BAZEN_SVETLO,
    KLIMA_CHLAZENI,
]
GROUP_RESIDENTS = "group.residents"

# Ovladace topeni


CLIMATE_DOMOV = "climate.domov"
CLIMATE_PETA = "climate.peta"
CLIMATE_BABICKA = "climate.babicka"
CLIMATE_LOZNICE = "climate.loznice"
CLIMATE_KUCHYNE = "climate.kuchyn"
CLIMATE_OBYVACI_POKOJ = "climate.obyvaci_pokoj"
CLIMATE_VASEK = "climate.vasek"
CLIMATE_STEPAN = "climate.stepan"
CLIMATE_KOUPELNA = "climate.koupelna"
CLIMATE_KOUPELNA_BABICKA = "climate.koup_ba"
TOPENI_MAX = "input_boolean.topeni_max"
GROUP_CLIMATE = [
    CLIMATE_BABICKA,
    CLIMATE_LOZNICE,
    CLIMATE_KUCHYNE,
    CLIMATE_OBYVACI_POKOJ,
    CLIMATE_VASEK,
    CLIMATE_STEPAN,
    CLIMATE_PETA,
    CLIMATE_KOUPELNA,
    CLIMATE_KOUPELNA_BABICKA,
]


TEST_ALARM = "input_boolean.test_alarm"


SWITCH_MASSAGE = "input_boolean.massage"


ON = "on"
OFF = "off"
ANO = "Ano"
NE = "Ne"
IDLE = "idle"

T_BINARY_EVENT = "binary_event"


HOME = "home"
NOT_HOME = "not_home"


POZADOVANO_ZAMCENO = "input_boolean.pozadovano_zamceno"
FIBARO_KONTROLUJE_HA = "input_boolean.kontrola_ze_strany_fibaro"  # fibaro kontroluje HA, timto se da vypnout


LIGHT_VENKOVNI_SVETLO = "light.venkovni_zarovka"
IS_VENKOVNI_SVETLO = "input_select.venkovni_zarovka"

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

UNAVAILABLE = "unavailable"
HEAT = "heat"
PLAYING = "playing"
PAUSED = "paused"
MIN_FIBARO_START = 160

# Events
E_ASS_EVENTS = []


E_API_ANO_NE = "E_API_ANO_NE"
E_API_GOOGLE = "E_API_GOOGLE"
E_CALL_SERVICE = "call_service"

E_DO_LOG = "E_DO_LOG"
E_ENTITY_ERROR = "E_ENTITY_ERROR"
E_FIBARO_GET_OPERATING_MODE = "E_FIBARO_GET_OPERATING_MODE"
E_FIBARO_PUBLISH_NOTIFICATIONS = "E_FIBARO_PUBLISH_NOTIFICATIONS"

E_MEDIA = "E_MEDIA"


E_TAKT = "E_TAKT"


E_TAG_OTEVRENI_DVERI = "E_OTEVRENI_DVERI"

E_WAKE_UP = "E_WAKE_UP"
E_BINARY_SENSOR = "E_BINARY_SENSOR"
E_START_NOC = "E_START_NOC"
E_END_NOC = "E_END_NOC"

E_TEST_APP = "E_TEST_APP"
E_OBYVAK_KLID = "E_OBYVAK_KLID"
E_OPUSTENI_DOMU = "E_OPUSTENI_DOMU"
E_GARAZ_ODCHOD = "E_GARAZ_ODCHOD"


C_DOMAIN = "domain"
C_PERSISTENT_NOTIFICATION = "persistent_notification"
C_FIBARO_ID = "fibaro_id"
C_DELETE_ALL = "delete_all"
C_TRIGGER = "trigger"
C_ENTITY = "entity"
C_VALUE = "value"
C_PROCEDURE = "procedure"
C_SWITCH_OFF = "switch_off"
C_SATELIT_KANAL = "kanal"
C_DVD = "dvd"
C_SAT = "sat"
C_PARAMS = "params"
C_MEDIA_OZNAM_ZACATEK = "oznam_zacatek"
C_MEDIA_OZNAM_KONEC = "oznam_konec"
C_AKVARIUM_KRMENI = "akvarium_krmeni"


C_ZAPNI_SHIELD = "zapni_shield"
C_NIKDO_UVNITR = "nikdo_uvnitr"

LETNI_CAS = "input_boolean.letni_cas"

TOPENI_VENTIL = "TopeniVentil"

DEVICE_TATA_MOBIL = "7cb1c96930bca825"


OBYVAK_TLUMENE_SVETLO = "input_boolean.obyvak_tlumene_svetlo"
ASS_DOBRE_RANO = "input_boolean.ass_dobre_rano"
ASS_VENKOVNI_POCASI = "input_boolean.ass_venkovni_pocasi"
ASS_ANO_NE = "input_boolean.ass_ano_ne"

takt_ready = False
