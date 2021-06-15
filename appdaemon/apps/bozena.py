from utils import BasicApp
from globals import ON, OFF, ANO, NE
import indego_const as igc
from sensor_op import AppBinarySensor
from helper_tools import MyHelp as h
import xml.etree.ElementTree as ET
import ntpath


C_MOVING = "Mowing"

SLOVNIK = {
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

GROUP_CALCULATE = [igc.MAP_0_X, igc.MAP_0_Y, igc.MAP_1_X, igc.MAP_1_Y]


class Bozena(BasicApp):
    def initialize(self):
        super().initialize()
        self.do_log = "input_boolean.log_bozena"
        self.my_log("Start bozena")
        self._const_x: float = 0.0
        self._const_y: float = 0.0

        self.listen_state(self._cti_stav, igc.BOZENA_MOWER_POSITION)
        self.listen_state(self._cti_stav, igc.BOZENA_STATE_DETAIL)
        for g in GROUP_CALCULATE:
            self.listen_state(self._calculate_init, g)
        # Definice prikazu, plus stavy, ktere rusi zapnute prikazy
        self._prikazy = {
            igc.BOZENO_SEKAT: [
                self._sekat,
                ("Mowing", "Border cut", "Mowing - Relocalising"),
            ],
            igc.BOZENO_DOMU: [self._domu, ("Sleeping", "Mowing - Paused")],
            igc.BOZENO_PAUZA: [self._pauza, ("Docking", "Mowing - Paused")],
        }

        for entity, ar in self._prikazy.items():
            self.listen_on(ar[0], entity)

        # Musi byt zadefinovano pred _cti_stav
        self._sensor_bozena_doma = AppBinarySensor(
            self,
            igc.BOZENA_DOMA,
            "Božena doma",
            OFF,
            "mdi:robot-mower",
            "mdi:alpha-p-box",
        )

        self.run_in(self._calculate_init, 2)
        # Stav, ktery se zobrazuje - zadefinovany jako sensor

        self.tlacitko(self._update_bozena, igc.IB_BOZENA_UPDATE)
        self.simple_loop(30)

    def _loop(self, *kwargs):
        self.my_log(f"State: {self._state}")
        if self._state != C_MOVING:
            return
        self._update_bozena()

    def _call_service(self, comm):
        self.my_log(f"Prikaz {comm}")
        self.my_log(self.call_service("indego/command", command=comm))

    @property
    def _state_detail(self):
        return self.get_state(igc.BOZENA_STATE_DETAIL)

    @property
    def _position(self):
        return self.get_state(igc.BOZENA_MOWER_POSITION)

    @property
    def _state(self):
        return self.get_state(igc.BOZENA_STATE)

    def _get_xy(self):
        try:
            retval = float(
                self.get_attr_state(igc.BOZENA_MOWER_POSITION, "svg_x_pos")
            ), float(self.get_attr_state(igc.BOZENA_MOWER_POSITION, "svg_y_pos"))
        except:
            retval = (0, 0)
        return retval

    @property
    def _je_doma(self):
        return self.get_state_str(igc.BOZENA_STATE) == "Docked"

    def _cti_stav(self, *kwargs):
        self.my_log("Cte stav")
        s = self._state_detail
        x, y = self._get_xy()
        nx = int(x * self._const_x)
        ny = int(y * self._const_y)
        self.my_log(f"Bozena x: {x} {nx} y: {y} {ny}")
        self.set_state(igc.MOWER_X, state=nx)
        self.set_state(igc.MOWER_Y, state=ny)
        for entity, ar in self._prikazy.items():
            if self.is_entity_on(entity) and s in ar[1]:
                self.turn_off(entity)

        if s in SLOVNIK.keys():
            self.my_log(f"Je ve slovniku {s}")
            self.set_sensor_state(igc.BOZENA_STATE_CZ, SLOVNIK[s])
        else:
            self.my_log(f"Neni ve slovniku {s}")
            self.set_state(igc.BOZENA_STATE_CZ, state=s)

        state = OFF
        if s in ("Docked", "Charging") or self._je_doma:
            state = ON
            self.turn_off(igc.BOZENO_DOMU)
        self.my_log(f"Nastaveni doma: {state}")
        self._sensor_bozena_doma.state = state
        # Kontrola, je-li splnen pozadavek zakaz sekani
        if (
            not self._je_doma
            and self.is_entity_on(igc.BOZENA_ZAKAZ_SEKANI)
            and self.is_entity_off(igc.BOZENO_DOMU)
        ):
            self.turn_on(igc.BOZENO_DOMU)

    def _prikaz(self, entity_id: str):
        self.my_log(f"entity_id: {entity_id}")
        for k in self._prikazy.keys():
            if k != entity_id:
                self.turn_off(k)
        self._cti_stav()

    def _sekat(self, entity_id):
        self._prikaz(entity_id)
        self._call_service("mow")

    def _pauza(self, entity_id):
        self._prikaz(entity_id)
        self._call_service("pause")

    def _domu(self, entity_id):
        self._prikaz(entity_id)
        self._call_service("returnToDock")

    def _update_bozena(self, *kwargs):
        try:
            self.my_log(self.call_service("indego/update_state"))
        except:
            pass

    def _calculate_init(self, *kwargs):
        map_picture = self.get_state(igc.MOWER_MAP)
        basename = ntpath.basename(map_picture)
        filename = f"/config/www/{basename}"
        svg = ET.parse(filename)
        root = svg.getroot()
        self.my_log(root.tag)
        rects = root.findall("{http://www.w3.org/2000/svg}rect")
        if len(rects) == 0:
            return
        width = float(rects[0].attrib["width"])
        height = float(rects[0].attrib["height"])
        x0 = self.get_state_float(igc.MAP_0_X)
        y0 = self.get_state_float(igc.MAP_0_Y)
        x1 = self.get_state_float(igc.MAP_1_X)
        y1 = self.get_state_float(igc.MAP_1_Y)
        self._const_x = (x1 - x0) / width
        self._const_y = (y0 - y1) / height
        self.my_log(f"width: {width} const_x: {self._const_x}")
        self.my_log(f"height: {height} const_x: {self._const_y}")
        self._cti_stav()
