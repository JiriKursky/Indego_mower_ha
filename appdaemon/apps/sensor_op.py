import appdaemon.plugins.hass.hassapi as hass
from globals import ON, OFF
from base_op import BaseOp, UObject
from utils import BasicApp
from helper_tools import StrOp, DateTimeOp, MyHelp as h
import datetime  # nutne
import adbase as ad


class DefineEntity:
    @staticmethod
    def create(parent: BaseOp, entity_id, **kwargs):
        if parent.entity_exists(entity_id):
            if not kwargs:
                kwargs: dict = {}
            kwargs.update({"state": parent.get_state(entity_id)})
        domain, name = StrOp.split_entity(entity_id)
        if domain == "sensor":
            return AppSensorState(
                parent,
                entity_id,
                h.par(kwargs, "state"),
                h.par(kwargs, "friendly_name"),
            )
        elif domain == "input_boolean":
            return AppInputBoolean(
                parent,
                entity_id,
                h.par(kwargs, "friendly_name", ""),
                h.par(kwargs, "state", False),
            )


class SensorOp(UObject):
    def __init__(self, parent: BaseOp, entity: str, friendly_name: str = ""):
        """Zakladni object

        Args:
            parent (BaseOp): parent
            entity (str): entity_id
            friendly_name (str, optional): nazev. Defaults to "".
        """
        super().__init__(parent)
        self.entity = entity
        if friendly_name:
            self.friendly_name = friendly_name
        else:
            self.friendly_name = entity

    @property
    def get_float(self) -> float:
        try:
            retval = float(self.state)
        except:
            retval = 0
        return retval


class AppInputNumber(SensorOp):
    def __init__(
        self,
        parent: BaseOp,
        entity: str,
        state: int,
        friendly_name: str = "",
        min_value: int = 0,
        max_value: int = 100,
    ):

        attr = {}
        attr.update(
            {
                "friendly_name": friendly_name,
                "min": min_value,
                "max": max_value,
                "step": 1,
                "mode": "box",
            }
        )
        parent.set_entity_state(entity, state, attr)


class AppInputBoolean(SensorOp):
    def __init__(
        self,
        parent: BaseOp,
        entity: str,
        friendly_name: str = "",
        state: bool = False,
    ):
        """Define input_boolean

        Args:
            parent (BaseOp): [description]
            entity (str): [description]
            friendly_name (str, optional): [description]. Defaults to "".
            state (bool, optional): [description]. Defaults to False.
        """

        attr = {}
        attr.update(
            {
                "friendly_name": friendly_name,
            }
        )
        parent.set_entity_state(entity, state, attr)


class AppSensorState(SensorOp):
    def __init__(
        self, parent: BaseOp, entity: str, state: str, friendly_name: str = ""
    ):
        """Definuje sensor se state

        Args:
            parent (BaseOp): parent
            entity (str): entita
            state (type): stav
            friendly_name (str, optional): nazev. Defaults to "".
        """
        super().__init__(parent, entity, friendly_name)
        parent.set_entity_state(entity, state, {"friendly_name": friendly_name})

    @property
    def state(self) -> str:
        return self.ba.get_state(self.entity)

    @state.setter
    def state(self, value: str):
        self.ba.set_entity_state(self.entity, value)


class AppBinarySensor(AppSensorState):
    def __init__(
        self,
        parent: BaseOp,
        entity: str,
        state: str,
        friendly_name: str = "",
        icon_on: str = "",
        icon_off: str = "",
        linked_entity: str = "",
    ):
        super().__init__(parent, entity, state, friendly_name)
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._linked_entity = linked_entity
        if linked_entity:
            parent.listen_on_off(self._listen_on_off, linked_entity)
            if parent.is_entity_on(linked_entity):
                self.state = ON
            else:
                self.state = OFF

    def _listen_on_off(self, yes):
        if yes:
            self.state = ON
        else:
            self.state = OFF

    @property
    def state(self) -> str:
        return self.ba.get_state(self.entity)

    @state.setter
    def state(self, value: str):
        self.ba.my_log(f"Binary {value}")
        self.ba.set_entity_state(self.entity, value)
        if value == ON and self._icon_on:
            self.ba.set_attribute(self.entity, {"icon": self._icon_on})
        elif value == OFF and self._icon_off:
            self.ba.set_attribute(self.entity, {"icon": self._icon_off})


class AppSensorNumber(AppSensorState):
    def __init__(
        self, parent: BaseOp, entity: str, friendly_name: str = "", default: int = 0
    ):
        super().__init__(parent, entity, str(default), friendly_name)

    @property
    def state(self) -> int:
        return int(self.ba.get_state(self.entity))

    @state.setter
    def state(self, value: int):
        self.ba.set_entity_state(self.entity, value)


class AppSensorTime(SensorOp):
    def __init__(self, parent: BaseOp, entity: str, friendly_name: str = ""):
        """Definice sensor casu
        pouziva se s funkci update_timestamp

        Args:
            parent (BaseOp): rodic
            entity (str): entita
            friendly_name (str, optional): nazev. Defaults to "".
        """
        super().__init__(parent, entity, friendly_name)
        self.state = self.ba.get_attr_state(entity, "last_updated")
        if not self.state:
            self.state = DateTimeOp.just_now()
        parent.set_entity_state(
            entity,
            self.state,
            {"friendly_name": self.friendly_name, "device_class": "timestamp"},
        )

    def timestamp(self, entity, state):
        self.ba.set_entity_state(
            entity,
            state,
            {"friendly_name": self.friendly_name, "device_class": "timestamp"},
        )

    def update_timestamp(self):
        """Provede update casoveho razitka sensoru"""
        state = f"{datetime.datetime.utcnow().isoformat()}+00:00"
        self.timestamp(self.entity, state)


class AppSensorTemperature(AppSensorState):
    def __init__(
        self, parent: BaseOp, entity: str, state: type, friendly_name: str = ""
    ):
        """Definuje sensor teploty

        Args:
            parent (BaseOp): parent
            entity (str): nazev entity
            state (type): stupne
            friendly_name (str, optional): nazev. Defaults to "".
        """

        super().__init__(parent, entity, state, friendly_name)

        parent.set_entity_state(
            entity,
            state,
            {
                "friendly_name": self.friendly_name,
                "device_class": "temperature",
                "unit_of_measurement": "°C",
            },
        )

    @property
    def state(self):
        return self.ba.get_state(self.entity)

    @state.setter
    def state(self, value):
        self.ba.set_state(
            self.entity,
            state=value,
            attributes={"device_class": "temperature", "unit_of_measurement": "°C"},
        )
