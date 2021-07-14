""" Bosch Indego Mower module """

from utils import BasicApp
import globals as g
import global_indego as igc
from helper_tools import MyHelp as h
from globals_def import constsDef as c, eventsDef as e

# used for svg parse
import xml.etree.ElementTree as ET
import ntpath


GROUP_CALCULATE = (igc.MAP_0_X, igc.MAP_0_Y, igc.MAP_1_X, igc.MAP_1_Y)


class IndegoMower(BasicApp):
    def initialize(self):
        super().initialize()
        self.log_button = "input_boolean.log_bozena"

        # Check sensor

        # Last coordinates before update
        self._last = (0, 0)

        # Specifies how many should ask for new update (position is the same and mower is mowing)
        self._update_counter = 0

        self.my_debug("Start indego_mower")

        self.create_entity(igc.MOWER_STATE_JS, linked_entity=igc.MOWER_STATE)
        self.create_entity(igc.LAWN_MOWED_JS, linked_entity=igc.LAWN_MOWED)
        self.create_entity(igc.MOWER_BATTERY_JS, linked_entity=igc.MOWER_BATTERY)
        self.create_entity(
            igc.MOWER_POSITION_JS,
            linked_entity=igc.MOWER_POSITION,
            linked_entity_copy_attributes=True,
        )

        self.turn_off(igc.BOZENA_UPDATE)
        self.listen_on(self._update_bozena, igc.BOZENA_UPDATE)
        self.listen_state_simple(self._cti_stav, igc.MOWER_POSITION)
        self.listen_state_simple(self._cti_stav, igc.MOWER_STATE_DETAIL)
        for g in GROUP_CALCULATE:
            self.my_debug(f"listen: {g}")
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

        for entity_id, ar in self._prikazy.items():
            self.listen_on(ar[0], entity_id)
        self.run_later(self._update_bozena)
        self.simple_loop(5)

    @property
    def _const_x(self):
        return self.get_state_float(igc.RATIO_X)

    @_const_x.setter
    def _const_x(self, value):
        self.set_entity_state(igc.RATIO_X, value)

    @property
    def _const_y(self):
        return self.get_state_float(igc.RATIO_Y)

    @_const_y.setter
    def _const_y(self, value):
        self.set_entity_state(igc.RATIO_Y, value)

    @property
    def _sensor_bozena_doma(self):
        return self.get_state_binary(igc.INDEGO_HOME)

    @_sensor_bozena_doma.setter
    def _sensor_bozena_doma(self, value: str):
        attributes = self.get_attributes(igc.INDEGO_HOME)
        if not attributes:
            attributes = {}
        if value == g.ON:
            attributes.update({"icon": "mdi:robot-mower"})
            self.set_state(igc.INDEGO_HOME, state=g.ON, attributes=attributes)
        else:
            attributes.update({"icon": "mdi:robot-mower"})
            self.set_state(igc.INDEGO_HOME, state=g.OFF, attributes=attributes)

    def loop(self, *kwargs) -> None:
        """Loop for update of position"""
        if self._state != c.Mowing:
            return
        self._update_bozena()

    def _call_service(self, comm):
        self.my_debug(f"Prikaz {comm}")
        try:
            self.call_service("indego_map/command", command=comm)
        except:
            pass

    @property
    def _state_detail(self):
        return self.get_state(igc.MOWER_STATE_DETAIL)

    @property
    def _position(self):
        return self.get_state(igc.MOWER_POSITION)

    @property
    def _state(self):
        return self.get_state(igc.MOWER_STATE)

    def _get_xy(self) -> tuple:
        """Reading parametres from sensor

        Returns:
            (tuple): (x,y)
        """
        try:
            retval = float(self.get_attr_state(igc.MOWER_POSITION, "svg_x_pos")), float(
                self.get_attr_state(igc.MOWER_POSITION, "svg_y_pos")
            )
        except:
            retval = (0, 0)
        self.my_debug(retval)
        return retval

    @property
    def _je_doma(self):
        return self.get_state_str(igc.MOWER_STATE) == "Docked"

    def _cti_stav_event(self, entity, attribute, old, new, kwargs):
        self._cti_stav()

    def _cti_stav(self, *kwargs):
        self.my_debug("Cte stav")
        if self._const_x == 0:
            self._calculate_init()

        self.turn_off(igc.BOZENA_UPDATE)
        s = self._state_detail
        x, y = self._get_xy()
        nx = int(x * self._const_x)
        ny = int(y * self._const_y)
        self.my_debug(f"Bozena x: {x} {nx} y: {y} {ny}")
        self.set_entity_state(igc.MOWER_X, nx)
        self.set_entity_state(igc.MOWER_Y, ny)
        for entity_id, ar in self._prikazy.items():
            if self.is_entity_on(entity_id) and s in ar[1]:
                self.turn_off(entity_id)

        if s in igc.TRANSLATE.keys():
            self.my_debug(f"Je ve slovniku {s}")
            self.set_entity_state(igc.BOZENA_STATE_INT, igc.TRANSLATE[s])
        else:
            self.my_debug(f"Neni ve slovniku {s}")
            self.set_entity_state(igc.BOZENA_STATE_INT, s)

        state = g.OFF
        if s in ("Docked", "Charging") or self._je_doma:
            state = g.ON
            self.turn_off(igc.BOZENA_DOMU)
        self.my_debug(f"Nastaveni doma: {state}")
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
        self.my_debug(f"entity_id: {entity_id}")
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
            self.call_service("indego_map/update_state")
        except:
            pass
        self._cti_stav()

    def _calculate_init(self, *kwargs):
        map_picture = self.get_state(igc.MOWER_MAP)
        self.my_debug(map_picture)
        if not map_picture:
            map_picture = "/local/indego_map.svg"
            self.call_service(
                "input_text/set_value", entity_id=igc.MOWER_MAP, value=map_picture
            )
            # self.set_entity_state(igc.MOWER_MAP, map_picture)
        basename = ntpath.basename(map_picture)
        filename = f"/config/www/{basename}"
        svg = ET.parse(filename)
        root = svg.getroot()
        self.my_debug(root.tag)
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
        self.my_debug(f"width: {width} const_x: {self._const_x}")
        self.my_debug(f"height: {height} const_x: {self._const_y}")

    def _calculate_listen(self, entity, attribute, old, new, kwargs):
        self.my_debug("Do calculate")
        self._calculate_init()
