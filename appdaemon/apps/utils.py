import datetime  # je potreba
import uuid
import time
from globals import (
    ON,
    OFF,
    PLAYING,
    HOME,
    UNAVAILABLE,
    C_TRIGGER,
    C_PROCEDURE,
    E_DO_LOG,
    C_PARAMS,
    IDLE,
    HEAT,
    E_ENTITY_ERROR,
    E_API_GOOGLE,
)
from globals_def import eventsDef as e
import globals as g
import appdaemon.plugins.hass.hassapi as hass
from helper_tools import DateTimeOp, MyHelp as h
from inspect import currentframe, getframeinfo
import location_obyvaci_pokoj as lop
from base_op import BaseOp


def defineLoop(has: object, callback: type, interval: int) -> list:
    """Definuje loop pres eventy, je zakomponovan v UObject

    Args:
        has (object): zdroj
        callback (type): callback
        interval (int): interval pro opakovani
    Returns:
        tuple: (nazev eventu, handler)
    """
    # Vytvoreni nazvu pro event
    event = str(uuid.uuid4())
    has.fire_event(e.DEF_LOOP, trigger=event, interval=interval)
    # Chytani loop
    handler = has.listen_event(callback, event)
    return [event, handler]


class BasicApp(BaseOp):
    def initialize(self):
        super().initialize()
        self._toggle_def = {}
        self._ovladac = {}
        self._async_run_update = False
        self._msg = ""

        self._events = {}
        self.def_sensors = {}

    def create_entity(self, entity_id: str, **kwargs) -> str:
        if "attributes" in kwargs:
            self.fire_event(
                "E_DEFINE_ENTITY", entity_id=entity_id, attributes=kwargs["attributes"]
            )
        else:
            self.fire_event("E_DEFINE_ENTITY", entity_id=entity_id)
        return entity_id

    def run_later(self, proc: type) -> None:
        """Pouziva se pro pozdejsi spusteni

        Args:
            proc (type): procedura, ktera bude pozdeji spustena
        """
        self.run_in(proc, 5)

    def simple_loop(self, interval: int, *kwargs) -> None:
        """loop definovany pres takt
        v modulu musi byt _loop(self) pripadne callback

        Args:
            interval (int): opakovani v sekundach
        """
        if kwargs:
            callback = kwargs[0]
        else:
            callback = self._loop
        self.my_log("Jdu definovat takt")
        self._loop_interval = interval
        self.run_in(self._start_loop, 2)

    def _start_loop(self, *kwargs):
        if not g.takt_ready:
            self.my_log("Takt neni pripraven")
            self.run_in(self._start_loop, 2)
            return
        defineLoop(self, self._loop, self._loop_interval)

    def _loop(self) -> None:
        """Volano pomoci simple_loop
        abstraktni funkce
        """
        pass

    def cancel_timer(self, handler):
        if not handler:
            return
        if self.timer_running(handler):
            # retval = self.info_timer(handler)
            super().cancel_timer(handler)

    def google_say(self, msg, temporary=False):
        self._msg = msg
        self.fire_event(E_API_GOOGLE, todo=msg, temporary=temporary)

        # self.run_in(self._say, 5)

    def _say(self, *kwargs):
        self.call_service(
            "tts/google_translate_say",
            entity_id="media_player.family_room_speaker",
            message=self._msg,
        )

    def entity_error(self, entity_id) -> bool:
        retval = self.get_state(entity_id) == UNAVAILABLE
        if retval:
            self.fire_event(E_ENTITY_ERROR, entity=entity_id)
            self.my_log(f"Error entita: {entity_id}")
        return retval

    def toggle(self, entity_id):
        if self.entity_error(entity_id):
            return False

        if self.is_entity_on(entity_id):
            self.turn_off(entity_id)
            return False
        else:
            self.turn_on(entity_id)
            return True

    def turn(self, entity_id, yes) -> bool:
        if self.entity_error(entity_id):
            return None
        if h.yes(yes):
            self.turn_on(entity_id)
            return True
        else:
            self.turn_off(entity_id)
        return False

    def switch_turn_on(self, entity_id):
        self.call_service("switch/turn_on", entity_id=entity_id)

    def switch_turn_off(self, entity_id):
        self.call_service("switch/turn_off", entity_id=entity_id)

    def switch_turn(self, entity_id, yes):
        if yes == True or yes == ON:
            self.switch_turn_on(entity_id)
        else:
            self.switch_turn_off(entity_id)

    def scene_turn_on(self, entity_id):
        self.call_service("scene/turn_on", entity_id=entity_id)

    def get_all_state(self, entity_id: str) -> type:
        """Vraci cely state vcetne atributů

        Args:
            entity_id (str): entita

        Returns:
            [type]: [description]
        """
        if self.entity_exists(entity_id):
            return self.get_state(entity_id, attribute="all")
        else:
            return None

    def get_attr_state_float(self, entity_id, attr) -> float:
        return float(self.get_attr_state(entity_id, attr))

    def get_attributes(self, entity_id: str) -> dict:
        all = self.get_all_state(entity_id)
        if all:
            return all["attributes"]
        else:
            return None

    def get_state_float(self, entity_id: str) -> float:
        """Prevod state na float

        Args:
            entity_id (str): [description]

        Returns:
            float: [description]
        """
        retval: float = 0
        try:
            retval = float(self.get_state(entity_id))
        except:
            retval = 0
        return retval

    def get_state_seconds(self, entity_id: str) -> int:
        """Vraci z prepoctu minuty na sekundy

        Args:
            entity_id (str): [description]

        Returns:
            int: vraci vteriny
        """
        return self.get_state_float(entity_id) * 60

    def get_state_int(self, entity_id: str) -> int:
        return int(self.get_state_float(entity_id))

    def get_state_binary(self, entity_id: str) -> bool:
        return self.get_state(entity_id) == ON

    def get_state_str(self, entity_id: str) -> str:
        return str(self.get_state(entity_id))

    def _uprav_cas(self, date_time_obj):
        if g.letni_cas:
            date_time_obj += datetime.timedelta(hours=2)
        else:
            date_time_obj += datetime.timedelta(hours=1)
        return date_time_obj

    def dif_time_sec_mysql(self, s_time: str):
        ted = DateTimeOp.just_now_sec()
        date_time_obj = datetime.datetime.strptime(s_time, "%Y-%m-%dT%H:%M:%S")
        date_time_obj = self._uprav_cas(date_time_obj)
        sec = time.mktime(date_time_obj.timetuple())
        return ted - sec

    def google_oznam(self, to_say):
        if self.is_entity_on(lop.PRITOMNOST):
            self.google_say(to_say)

    def set_datetime(self, entity_id, time):
        time_to_set = time.strftime("%Y-%m-%d %H:%M:%S")
        self.set_entity_state(entity_id, time_to_set)
        self.call_service(
            "input_datetime/set_datetime", entity_id=entity_id, datetime=time_to_set
        )

    def set_attribute(self, entity: str, attr):
        """Nastaví nové atributy

        Args:
            entity ([type]): [description]
            attr ([type]): [description]
        """
        all = self.get_all_state(entity)
        state = all["state"]
        o_attr = all["attributes"]
        # Pridava atributy je starym
        for a in attr:
            o_attr[a] = attr[a]
        self.set_state(entity, state=state, attributes=o_attr)

    def listen_toggle(self, switch, button):
        self._toggle_def[button] = switch
        self.my_log("Switch {}".format(switch))
        self.listen_state(self._listen_toggle, button, new=ON)

    def _listen_toggle(self, entity, attribute, old, new, kwargs):
        switch = self._toggle_def[entity]
        self.my_log("Switch {}".format(switch))
        self.toggle(switch)

    # Update entity
    def force_update(self, entity_id):
        if self._async_run_update:
            self.my_log("Already in process")
            return
        self._async_run_update = True
        self.call_service("homeassistant/update_entity", entity_id=entity_id)
        self._async_run_update = False

    def _catch_tlacitko_on(self, entity, attribute, old, new, kwargs):
        self.my_log(f"Chyceno {entity}, {old}, {new}")
        trigger = h.par(self._events[entity], C_TRIGGER)
        if trigger:
            self.my_log(f"Fired {trigger}")
            params = h.par(self._events[entity], C_PARAMS)
            if params:
                self.fire_event(trigger, params)
            else:
                self.fire_event(trigger)
            # proc = h.par(self._events[entity], C_PROCEDURE)
            # if proc:
            #    self.my_log(f"Bude volana: {proc}")
            #    self.run_in(proc, 1)

    def _get_proc(self, trigger):
        for e in self._events:
            if self._events[e][C_TRIGGER] == trigger:
                return self._events[e][C_PROCEDURE]
        return None

    def _catch_event(self, *kwargs):
        self.my_log(f"Chyceno {kwargs[0]}")
        proc = self._get_proc(kwargs[0])
        if proc:
            self.my_log(f"Volana {proc}")
            self.run_in(proc, 1)

    def binary_tlacitko(self, proc, entity_id, **kwargs):
        self.my_log(f"entity: {entity_id}")
        trigger = h.par(kwargs, C_TRIGGER)
        if trigger:
            self._events[entity_id] = {C_TRIGGER: trigger, C_PROCEDURE: proc}
            self.listen_event(self._catch_event, trigger)
            self.listen_state(self._catch_tlacitko_on, entity_id, new=ON)
        else:
            self.listen_state(proc, entity_id, new=ON)

    def tlacitko(self, par_1: type = None, par_2: type = None) -> None:
        """Nastavi listening na par_1, pri par_2 string

        Args:
            par_1 (type, optional): procedura, ktera bude volana. Defaults to None.
            par_2 (type, optional): input_boolean. Defaults to None.
        """
        if not par_1 and not par_2:
            self.my_log("Kriticka chyba")

        proc = None
        if h.is_string(par_1) and callable(par_2):
            entity_id = par_1
            proc = par_2
        elif h.is_string(par_2) and callable(par_1):
            entity_id = par_2
            proc = par_1
        elif h.is_string(par_1):
            entity_id = par_1

        elif h.is_string(par_2):
            entity_id = par_2
        else:
            self.my_log("Kriticka chyba")

        # Jen inicializace - prepne na off
        if self.is_entity_on(entity_id):
            try:
                self.turn_off(entity_id)
            except:
                pass

        self.listen_state(self._tlacitko, entity_id, new=ON)
        if callable(proc):
            self.my_log(f"Ma proc: {entity_id}")
            self.listen_state(proc, entity_id, new=ON)

    def tlacitka(self, def_tlacitka: dict):
        """Hromadne zadefinovani tlacitek

        Args:
            def_tlacitka (dict): {input_boolean: proc}
        """
        for item in def_tlacitka.items():
            self.tlacitko(item[1], item[0])

    def _tlacitko(self, entity, attribute, old, new, kwargs):
        self.fire_event(e.TLACITKO, entity=entity)
        try:
            self.turn_off(entity)
        except:
            pass

    def ovladac_switch(self, input_boolean, switch):
        self._ovladac[input_boolean] = switch
        self.listen_state(self._ovladac_switch, input_boolean)

    def _ovladac_switch(self, entity, attribute, old, new, kwargs):
        switch = self._ovladac[entity]
        self.turn(switch, new)

    def _turn_off(self, entity):
        try:
            self.turn_off(entity)
        except:
            self.my_log("Turn off failed: {}".format(entity))

    def get_counter(self, entity):
        try:
            retVal = self.get_state(entity)
        except:
            retVal = 0
        return retVal

    def counter_increment(self, entity):
        retVal = True
        try:
            self.call_service("counter/increment", entity_id=entity)
        except:
            retVal = False
        return retVal

    def counter_reset(self, entity):
        retVal = True
        try:
            self.call_service("counter/reset", entity_id=entity)
        except:
            retVal = False
        return retVal

    def set_input_select(self, entity, value):
        retVal = True
        try:
            self.call_service(
                "input_select/select_option", entity_id=entity, option=value
            )
        except:
            retVal = False
        return retVal

    def set_input_number(self, entity: str, value: float):
        retVal = True
        try:
            self.call_service(
                "input_number/set_value", entity_id=entity, value=float(value)
            )
        except:
            retVal = False
        return retVal
