import appdaemon.plugins.hass.hassapi as hass
from helper_tools import DateTimeOp, MyHelp as h
import globals as g
from globals import ON, OFF
from inspect import currentframe, getframeinfo


class UObject(object):
    """Jednoduchy podobjekt majici parent a my_log

    Args:
        object ([type]): [description]
    """

    def __init__(self, parent: type):
        self.ba = parent

    def my_log(self, msg):
        self.ba.my_log(msg)


class BaseOp(hass.Hass):
    def initialize(self):
        self.do_log = False
        self.log("Ini: {}".format(DateTimeOp.just_now().strftime("%Y-%m-%d %H:%M:%S")))
        self._log_button = ""
        self._fired_proc_buff = []
        self._fired_proc = {}

    @property
    def letni_cas(self):
        return self.is_entity_on(g.LETNI_CAS)

    def listen_on_off(self, proc: type, entity_id: str) -> type:
        """Reaguje na on off a volá proc

        Args:
            proc (type): Volaná funkce
            entity_id (str): entita

        Returns:
            type: type: handler
        """

        self._fired_proc[entity_id] = proc
        return self.listen_state(self._fired_on_off, entity_id)

    def _fired_on_off(self, entity, attribute, old, new, kwargs):
        self.my_log(f"fired _on_off {old} {new}")
        if not entity in self._fired_proc:
            self.my_log("Systemova chyba")
            return
        proc = self._fired_proc[entity]
        if h.zmena_on(old, new):
            proc(True)
        elif h.zmena_off(old, new):
            proc(False)

    def _push_fired_proc(
        self, source: object, callback: object, entity_id: str, **kwargs
    ):
        self._fired_proc_buff.append((entity_id, source.__name__, callback))
        self.my_log(f"buffer pridano: {self._fired_proc_buff}, kwargs: {kwargs}")
        self.listen_state(source, entity_id, **kwargs)

    def _pop_fired_proc(self, entity: str, source: object):
        name = source.__name__
        self.my_log(f"porovnavam {entity}, {name} v {self._fired_proc_buff}")
        for e, s, c in self._fired_proc_buff:
            if (e == entity) and name == s:
                return c
        return None

    def _fired_off(self, entity, attribute, old, new, kwargs):
        c = self._pop_fired_proc(entity, self._fired_off)
        if callable(c):
            c(entity)

    def listen_off(self, def_proc: object, entity_id: str = None) -> type:
        """Reaguje na on volá proc

        Args:
            proc (type): Volaná funkce nebo dict
            entity_id (str): entita
        Example:
            prikazy = {
                lza.BOZENA_SEKAT: self._sekat,
                lza.BOZENA_DOMU: self._domu,
                lza.BOZENA_PAUZA: self._pauza,
            }
            self.listen_on(self._prikazy)
            nebo
            self.listen_on(self._prikaz, "enitiy_id")
        Returns:
            type: handler
        """
        if callable(def_proc):
            self._push_fired_proc(self._fired_off, def_proc, entity_id, new=OFF)
        elif h.is_dict(def_proc):
            retval = []
            for item in def_proc.items():
                retval.append(self.listen_on(item[1], item[0]))
            return retval

    def listen_on(self, def_proc: type, entity_id: str = None) -> type:
        """Reaguje na on  volá proc

        Args:
            proc (type): Volaná funkce nebo dict
            entity_id (str): entita
        Example:
            prikazy = {
                lza.BOZENA_SEKAT: self._sekat,
                lza.BOZENA_DOMU: self._domu,
                lza.BOZENA_PAUZA: self._pauza,
            }
            self.listen_on(self._prikazy)
            nebo
            self.listen_on(self._prikaz, "enitiy_id")
        Returns:
            type: handler
        """
        if callable(def_proc):
            self._fired_proc[entity_id] = def_proc
            return self.listen_state(self._fired_on, entity_id, new=ON)
        elif h.is_dict(def_proc):
            retval = []
            for item in def_proc.items():
                retval.append(self.listen_on(item[1], item[0]))
            return retval

    def _fired_on(self, entity, attribute, old, new, kwargs):
        if not entity in self._fired_proc:
            self.my_log("Systemova chyba")
            return
        proc = self._fired_proc[entity]
        if callable(proc):
            proc(entity)

    def listen_entity_on_off(self, proc, entity_id):
        self._fired_proc[entity_id] = proc
        return self.listen_state(self._fired_entity_on_off, entity_id)

    def _fired_entity_on_off(self, entity, attribute, old, new, kwargs):
        self.my_log(f"{old} {new}")
        if not entity in self._fired_proc:
            self.my_log("Systemova chyba")
            return
        proc = self._fired_proc[entity]
        if h.zmena_on(old, new):
            proc(entity, True)
        elif h.zmena_off(old, new):
            proc(entity, False)

    @property
    def log_button(self):
        return self._log_button

    def _my_log(self, message):
        cf = currentframe()
        line = cf.f_back.f_lineno
        cf = cf.f_back
        previous = cf.f_back.f_lineno
        self.log(f"{previous}: {message}")

    def my_log(self, message):
        if self.do_log:
            self._my_log(message)

    @log_button.setter
    def log_button(self, value):
        if self.entity_exists(value):
            self._log_button = value
            self.do_log = self.is_entity_on(value)
            self._my_log(f"Listener {value}")
            self.listen_on_off(self._turn_log, value)

    def _turn_log(self, yes):
        self._my_log(f"Log button {self._log_button} nastaven na {yes}")
        self.do_log = yes

    def is_entity_on(self, entity_id):
        state = self.get_state(entity_id)
        return (state == ON) or (state == "home") or (state == g.PLAYING)

    def is_entity_off(self, entity_id):
        return not self.is_entity_on(entity_id)

    def get_attr_state(self, entity_id: str, attr: str) -> type:
        """Vraci konkretni atribut

        Args:
            entity_id (str): [description]
            attr (str): [description]

        Returns:
            [type]: atribut
        """
        try:
            retval = self.get_state(entity_id, attribute=attr)
        except:
            retval = None
        return retval

    def set_entity_state(
        self, entity_id: str, state: type, attributes: dict = {}
    ) -> None:
        """Setting entity state

        Args:
            entity_id (str): [description]
            state (type): [description]
        """
        s_state: str = ""
        if h.is_string(state):
            s_state = state
        elif h.is_bool(state):
            if state:
                s_state = ON
            else:
                s_state = OFF
        else:
            s_state = str(state)
        if attributes:
            self.set_state(entity_id, state=s_state, attributes=attributes)
        else:
            self.set_state(entity_id, state=s_state)
