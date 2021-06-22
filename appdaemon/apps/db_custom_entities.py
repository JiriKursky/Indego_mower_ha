from utils import BaseOp
from tinydb import TinyDB, Query
from helper_tools import MyHelp as h

CUSTOM_ENTITIES = "/config/custom_entities.json"


class DbCustomEntities(BaseOp):
    def initialize(self):
        super().initialize()
        self.log_button = "input_boolean.log_db_custom_entities"
        self._db = TinyDB(CUSTOM_ENTITIES)
        self._query = Query()

    def get_raw_data(self, entity_id):
        result = self._db.search(self._query.entity_id == entity_id)
        if result:
            return result[0]
        else:
            return None

    def get_data(self, entity_id: str) -> dict:
        data = self.get_raw_data(entity_id)
        self.my_log(f"Result raw: {entity_id} {data}")
        if not data:
            return None
        state = h.par(data, "state")
        h.pop(data, ("entity_id", "state"))
        retval: dict = {"state": state, "attributes": data}
        return retval

    def get_state(self, entity_id):
        result = self.get_data(entity_id)
        if result:
            retval = result["state"]
        else:
            retval = None
        return retval

    def get_attributes(self, entity_id: str) -> type:
        try:
            attr = self.get_attributes(entity_id)
        except Exception as e:
            self.my_log(e)
            retval = self.get_data(entity_id)
            if retval:
                attr = retval["attributes"]
            else:
                return None
        return attr

    def replace_data(self, entity_id, state: type, attributes: dict = {}):
        attr = self.get_attributes(entity_id)
        self.my_log(f"Attributes from db: {attr}")
        if attr and attributes:
            attr.update(attributes)
        elif not attr:
            attr = attributes
        self._db.remove(self._query.entity_id == entity_id)
        self.set_state(entity_id, state=state, attributes=attr)
        attr.update({"state": state, "entity_id": entity_id})
        self._db.insert(attr)
