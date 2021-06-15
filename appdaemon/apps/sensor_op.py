from globals import ON, OFF
from base_op import BaseOp, UObject
from utils import BasicApp
from helper_tools import DateTimeOp
import datetime  # nutne


def UpdateEntity(parent: BaseOp, entity: str):
    parent.call_service("homeassistant/update_entity", entity_id=entity)


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

    def set_sensor_state(self, state: str, attr: dict):
        self.ba.set_state(self.entity, state=state, attributes=attr)

    @property
    def get_float(self) -> float:
        try:
            retval = float(self.state)
        except:
            retval = 0
        return retval


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
        self.set_sensor_state(state, {"friendly_name": self.friendly_name})

    @property
    def state(self) -> str:
        return self.ba.get_state(self.entity)

    @state.setter
    def state(self, value: str):
        self.ba.set_state(self.entity, state=value)


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
        self.ba.set_state(self.entity, state=value)
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
        self.ba.set_state(self.entity, state=str(value))


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
        self.set_sensor_state(
            self.state,
            {"friendly_name": self.friendly_name, "device_class": "timestamp"},
        )

    def timestamp(self, entity, state):
        self.set_sensor_state(
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

        self.set_sensor_state(
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
