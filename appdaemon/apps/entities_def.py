from utils import BasicApp
from globals import ON, OFF
import importlib
from helper_tools import StrOp
from tinydb import TinyDB, Query
from helper_tools import MyHelp as h

E_DEFINE_ENTITY = "E_DEFINE_ENTITY"


class EntitiesDef(BasicApp):
    def initialize(self):
        self.do_log = "input_boolean.entities_def_debug"
        self._entities: list = []
        self._db = TinyDB("custom.json")
        self._query = Query()
        self.listen_event(self._create, E_DEFINE_ENTITY)
        self.listen_event(self._change_state, event="call_service")

    def _db_get_raw_data(self, entity_id):
        result = self._db.search(self._query.entity_id == entity_id)
        if result:
            return result[0]
        else:
            return None

    def _db_get_data(self, entity_id: str):
        data = self._db_get_raw_data(entity_id)
        self.my_log(f"Result raw: {entity_id} {data}")
        if not data:
            return None
        state = h.par(data, "state")
        h.pop(data, ("entity_id", "state"))
        retval: dict = {"state": state, "attributes": data}
        return retval

    def _db_get_state(self, entity_id):
        result = self._db_get_data(entity_id)
        if result:
            retval = result["state"]
        else:
            retval = None
        return retval

    def _db_get_attributes(self, entity_id: str) -> type:
        try:
            attr = self.get_attributes(entity_id)
        except Exception as e:
            self.my_log(e)
            retval = self._db_get_data(entity_id)
            if retval:
                attr = retval["attributes"]
            else:
                return None
        return attr

    def _db_replace_data(self, entity_id, state: type, attributes: dict = {}):
        attr = self._db_get_attributes(entity_id)
        self.my_log(f"Attributes from db: {attr}")
        if attr and attributes:
            attr.update(attributes)
        elif not attr:
            attr = attributes

        self.my_log(f"Attributes 2: {attr}")
        self._db.remove(self._query.entity_id == entity_id)
        self.set_state(entity_id, state=state, attributes=attr)
        attr.update({"state": state, "entity_id": entity_id})
        self.my_log(f"Insert: {attr}")
        self._db.insert(attr)

    def _create(self, event, data, kwargs):
        self.my_log(data)
        entity_id = h.par(data, "entity_id")
        attributes = h.par(data, "attributes", {})
        # Is it saved?
        state = self._db_get_state(entity_id)
        if not state:
            state = h.par(data, "state", "")
        self.my_log(f"Creating: {entity_id} state: {state} attr: {attributes}")
        domain, name = StrOp.split_entity(entity_id)
        if domain == "input_boolean":
            self._input_boolean(entity_id, state, attributes)
        elif domain == "sensor" or domain == "binary_sensor":
            self._sensor(entity_id, state, attributes)
        elif domain == "input_number":
            self._input_number(entity_id, state, attributes)
        elif domain == "input_text":
            self._input_text(entity_id, state, attributes)

    def _input_boolean(self, entity_id: str, state: type, attributes: dict):
        self._entities.append(entity_id)
        if not self.entity_exists(entity_id):
            self.set_state(entity_id, state=OFF)

    def _sensor(self, entity_id, state, attributes):
        if attributes:
            self.set_state(entity_id, state=state, attributes=attributes)
        else:
            self.set_state(entity_id, state=state)

    def _change_state(self, event_name, data, kwargs):
        try:
            entity = data["service_data"]["entity_id"]
        except:
            return
        if not entity in self._entities:
            return
        domain, _ = StrOp.split_entity(entity)
        if domain == "input_number":
            self.my_log(data["service"])
        if data["service"] == "decrement":
            state = self.get_state_int(entity)
            state -= 1
            self.set_state(entity, state)
        if data["service"] == "set_value":
            state = data["service_data"]["value"]
            self.my_log(f"Replace to: {state}")
            self._db_replace_data(entity, state)
        if data["service"] == "turn_off":
            state = OFF
            self.set_state(entity, state=state)
            self._db_replace_data(entity, state)
        if data["service"] == "turn_on":
            state = ON
            self.set_state(entity, state=state)
            self._db_replace_data(entity, state)

    def _input_number(self, entity_id, state, attributes):
        """State je jiz preneseno z databaze

        Args:
            entity_id ([type]): [description]
            state ([type]): [description]
            attributes ([type]): [description]
        """
        _, friendly_name = StrOp.split_entity(entity_id)
        attributes_default: dict = {
            "initial": "null",
            "editable": "true",
            "min": 1,
            "max": 100,
            "step": 1,
            "mode": "box",
            "unit_of_measurement": "min",
            "friendly_name": friendly_name,
        }
        if attributes:
            attributes_default.update(attributes)

        self.my_log(f"State from databaze: {state}")
        if not state:
            state = attributes_default["min"]
        self.my_log(f"Prenos state: {state}")
        self._db_replace_data(entity_id, state, attributes_default)

        if self.entity_exists(entity_id):
            self.my_log(f"Existuje entita {entity_id}")
            if not entity_id in self._entities:
                self._entities.append(entity_id)
            return
        elif not entity_id in self._entities:
            self._entities.append(entity_id)

    def _input_text(self, entity_id, state, attributes):
        """State je jiz preneseno z databaze

        Args:
            entity_id ([type]): [description]
            state ([type]): [description]
            attributes ([type]): [description]
        """
        _, friendly_name = StrOp.split_entity(entity_id)
        attributes_default: dict = {
            "editable": "true",
            "min": 0,
            "max": 100,
            "patern": "null",
            "mode": "text",
            "friendly_name": friendly_name,
        }
        if attributes:
            attributes_default.update(attributes)

        self.my_log(f"State from databaze: {state}")
        if not state:
            state = ""
        self.my_log(f"Prenos state: {state}")
        self._db_replace_data(entity_id, state, attributes_default)

        if self.entity_exists(entity_id):
            self.my_log(f"Existuje entita {entity_id}")
            if not entity_id in self._entities:
                self._entities.append(entity_id)
            return
        elif not entity_id in self._entities:
            self._entities.append(entity_id)
