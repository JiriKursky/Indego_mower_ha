from utils import BasicApp
from globals import ON, OFF, ANO, NE
import indego_const as igc
from helper_tools import MyHelp as h
import xml.etree.ElementTree as ET
import ntpath


GROUP_CALCULATE = (igc.MAP_0_X, igc.MAP_0_Y, igc.MAP_1_X, igc.MAP_1_Y)


class Bozena(BasicApp):
    def initialize(self):
        super().initialize()
        self.log_button = "input_boolean.log_bozena"
        for e in igc.ENTITIES_PX:
            self.create_entity(e, attributes={"unit_of_measurement": "px", "max": 2000})
        for e in igc.DEF_ENTITIES:
            self.create_entity(e[0], attributes={"friendly_name": e[1]})

        # Last coordinates before update
        self._last = (0, 0)

        # Specifies how many should ask for new update (position is the same and mower is mowing)
        self._update_counter = 0

        self.my_log("Start bozena")
        self._const_x: float = 0.0
        self._const_y: float = 0.0

        self.listen_state(self._cti_stav, igc.BOZENA_MOWER_POSITION)
        self.listen_state(self._cti_stav, igc.BOZENA_STATE_DETAIL)
        for g in GROUP_CALCULATE:
            self.listen_state(self._calculate_listen, g)
        # Definice prikazu, plus stavy, ktere rusi zapnute prikazy
        self._prikazy = {
            igc.BOZENA_SEKAT: [
                self._sekat,
                ("Mowing", "Border cut", "Mowing - Relocalising"),
            ],
            igc.BOZENA_DOMU: [self._domu, ("Sleeping", "Mowing - Paused")],
            igc.BOZENA_PAUZA: [self._pauza, ("Docking", "Mowing - Paused")],
        }

        for entity, ar in self._prikazy.items():
            self.listen_on(ar[0], entity)

        # Musi byt zadefinovano pred _cti_stav
        """
        self.create_entity(
            igc.BOZENA_DOMA,
            state=OFF,
            attributes={"friendly_name": "Božena doma", "icon": "mdi:robot-mower"},
        )
        """

        self.run_in(self._calculate_init, 20)
        # Stav, ktery se zobrazuje - zadefinovany jako sensor

        self.listen_on(self._update_bozena, igc.BOZENA_UPDATE)
        self.turn_off(igc.BOZENA_UPDATE)
        self.simple_loop(30)

    @property
    def _sensor_bozena_doma(self):
        return self.get_state_binary(igc.BOZENA_DOMA)

    @_sensor_bozena_doma.setter
    def _sensor_bozena_doma(self, value: str):
        attributes = self.get_attributes(igc.BOZENA_DOMA)
        if not attributes:
            return
        if value == ON:
            attributes.update({"icon": "mdi:robot-mower"})
            self.set_state(igc.BOZENA_DOMA, state=ON, attributes=attributes)
        else:
            attributes.update({"icon": "mdi:robot-mower"})
            self.set_state(igc.BOZENA_DOMA, state=OFF, attributes=attributes)

    def _loop(self, *kwargs):
        # self.my_log(f"State: {self._state}")
        if self._state != igc.C_MOVING:
            return
        self._update_bozena()

    def _call_service(self, comm):
        self.my_log(f"Prikaz {comm}")
        self.call_service("indego/command", command=comm)

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
        self.turn_off(igc.BOZENA_UPDATE)
        s = self._state_detail
        x, y = self._get_xy()
        nx = int(x * self._const_x)
        ny = int(y * self._const_y)
        self.my_log(f"Bozena x: {x} {nx} y: {y} {ny}")
        self.set_entity_state(igc.MOWER_X, nx)
        self.set_entity_state(igc.MOWER_Y, ny)
        for entity, ar in self._prikazy.items():
            if self.is_entity_on(entity) and s in ar[1]:
                self.turn_off(entity)

        if s in igc.TRANSLATE.keys():
            self.my_log(f"Je ve slovniku {s}")
            self.set_entity_state(igc.BOZENA_STATE_CZ, igc.TRANSLATE[s])
        else:
            self.my_log(f"Neni ve slovniku {s}")
            self.set_entity_state(igc.BOZENA_STATE_CZ, s)

        state = OFF
        if s in ("Docked", "Charging") or self._je_doma:
            state = ON
            self.turn_off(igc.BOZENA_DOMU)
        self.my_log(f"Nastaveni doma: {state}")
        self._sensor_bozena_doma = state
        # Kontrola, je-li splnen pozadavek zakaz sekani
        if (
            not self._je_doma
            and self.is_entity_on(igc.BOZENA_ZAKAZ_SEKANI)
            and self.is_entity_off(igc.BOZENA_DOMU)
        ):
            self.turn_on(igc.BOZENA_DOMU)
        if (x, y) == self._last and self._update_counter > 0:
            self._update_counter -= 1
            self.run_in(self._update_bozena, 2)
        elif (x, y) != self._last:
            self._update_counter = 2

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
        self._last = self._get_xy()
        self.my_log(self._last)
        try:
            self.call_service("indego/update_state")
        except:
            pass

    def _calculate_init(self, *kwargs):
        map_picture = self.get_state(igc.MOWER_MAP)
        self.my_log(map_picture)
        if map_picture == "":
            map_picture = "/local/indego_map.svg"
            self.set_entity_state(igc.MOWER_MAP, map_picture)
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

    def _calculate_listen(self, entity, attribute, old, new, kwargs):
        self._calculate_init()
