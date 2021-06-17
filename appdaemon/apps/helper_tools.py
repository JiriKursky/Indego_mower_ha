import datetime
import time
import globals as g
from globals import ON, OFF


class StrOp:
    def __init__(self):
        pass

    @staticmethod
    def split_entity(entity: str) -> tuple:
        """Divide to namespace and entity

        Args:
            entity (str): [description]

        Returns:
            tuple: (namespace,entity_name)
        """
        return entity.split(".")

    @staticmethod
    def entity_name(entity: str) -> str:
        ret_val = StrOp.split_entity(entity)
        return ret_val[1]

    @staticmethod
    def str_time_to_sec(s_time=str):
        if s_time == g.UNAVAILABLE:
            return None
        try:
            date_time_obj = datetime.datetime.strptime(
                s_time, "%Y-%m-%dT%H:%M:%S.%f+00:00"
            )
        except:
            date_time_obj = None
        if not date_time_obj:
            try:
                date_time_obj = datetime.datetime.strptime(
                    s_time, "%Y-%m-%d %H:%M:%S.%f+00:00"
                )
            except:
                date_time_obj = None
        if not date_time_obj:
            try:
                date_time_obj = datetime.datetime.strptime(
                    s_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            except:
                date_time_obj = None

        if not date_time_obj:
            return 0
        date_time_obj += datetime.timedelta(hours=1)
        sec = int(time.mktime(date_time_obj.timetuple()))
        return sec


class MyHelp:
    def __init__(self):
        pass

    @staticmethod
    def is_array(myvar):
        return isinstance(myvar, list) or isinstance(myvar, tuple)

    @staticmethod
    def is_bool(myvar):
        return isinstance(myvar, bool)

    @staticmethod
    def is_dict(myvar):
        return isinstance(myvar, dict)

    @staticmethod
    def is_tuple(myvar):
        return isinstance(myvar, tuple)

    @staticmethod
    def is_string(myvar):
        return isinstance(myvar, str)

    @staticmethod
    def in_array(to_search, arr):
        try:
            a = arr.index(to_search)
            return True
        except:
            return False

    @staticmethod
    def attr(attributes):
        return {key: None for key in attributes}

    @staticmethod
    def pop(param: dict, key: type):
        if MyHelp.is_array(key):
            retval: list = []
            for k in key:
                retval.append(MyHelp.pop(param, k))
        else:
            try:
                param.pop(key)
            except:
                pass

    @staticmethod
    def par(param: dict, k: type, default: type = None) -> type:
        """Returning value from dicionary

        Args:
            param (dict): [description]
            k (type): [description]
            default (type, optional): [description]. Defaults to None.

        Returns:
            type: [description]
        """
        if not param:
            return default
        if MyHelp.is_array(k):
            ret_val = []
            for j in k:
                ret_val.append(MyHelp.par(param, j))
            return ret_val
        if k in param:
            return param[k]
        else:
            return default

    @staticmethod
    def vrat_on_off(yes: bool) -> str:
        if yes:
            return ON
        return OFF

    @staticmethod
    def kwarg_split(kwargs, param):
        if MyHelp.is_array(param):
            ret_val = []
            for p in param:
                ret_val.append(MyHelp.kwarg_split(kwargs, p))
            return ret_val
        k = kwargs[1]
        return MyHelp.par(k, param)

    @staticmethod
    def yes(value):
        return value == True or value == ON or value == g.PLAYING or value == g.HEAT

    @staticmethod
    def zmena_on(old, new):
        return (
            ((old == OFF) or (old == g.IDLE))
            and ((new == ON or new == g.PLAYING))
            or ((old == OFF) and (new == g.HEAT))
        )

    @staticmethod
    def zmena_off(old, new):
        return (old == ON or old == g.PLAYING) and (new == OFF or new == g.IDLE)


class DateTimeOp:
    def __init__(self):
        pass

    @staticmethod
    def just_now():
        return datetime.datetime.now()

    @staticmethod
    def just_now_sec():
        dnes = DateTimeOp.just_now()
        dnes_sec = time.mktime(dnes.timetuple())

        return dnes_sec

    @staticmethod
    def in_interval(start_time=str, end_time=str, compare=str) -> bool:
        i_start_time = StrOp.str_time_to_sec(start_time)
        i_end_time = StrOp.str_time_to_sec(start_time)
        i_compare = StrOp.str_time_to_sec(compare)
        return (i_compare >= i_start_time) and (i_compare <= i_end_time)

    @staticmethod
    def get_all_state(hass, entity_id):
        return hass.get_state(entity_id, attribute="all")

    @staticmethod
    def get_last_update(hass, entity_id):
        all_state = DateTimeOp.get_all_state(hass, entity_id)
        s_last_updated = all_state["last_updated"][
            :19
        ]  # 2019-08-05T19:22:40.626824+00:00
        lu = datetime.datetime.strptime(s_last_updated, "%Y-%m-%dT%H:%M:%S")
        return lu + datetime.timedelta(hours=2)

    @staticmethod
    def get_update_dif(hass, entity_id):
        last_updated = DateTimeOp.get_last_update(hass, entity_id)
        return DateTimeOp.just_now() - last_updated

    @staticmethod
    def _uprav_cas(date_time_obj, letni_cas: bool):
        if letni_cas:
            date_time_obj += datetime.timedelta(hours=2)
        else:
            date_time_obj += datetime.timedelta(hours=1)
        return date_time_obj

    @staticmethod
    def get_last_changed(basicApp, entity_id: str, letni_cas: bool):
        date_time_str = basicApp.get_attr_state(entity_id, "last_changed")
        # 2019-11-22T12:36:12.340577+00:00
        if date_time_str is None:
            return None
        date_time_obj = datetime.datetime.strptime(
            date_time_str, "%Y-%m-%dT%H:%M:%S.%f+00:00"
        )
        date_time_obj = DateTimeOp._uprav_cas(date_time_obj, letni_cas)
        return date_time_obj

    @staticmethod
    def get_last_changed_sec(hass: type, entity_id: str, letni_cas: bool) -> float:
        """Vraci zmenu od pocatku roku 1900

        Args:
            hass (bool): [description]
            entity_id ([type]): [description]

        Returns:
            float: [description]
        """
        date_time_obj = DateTimeOp.get_last_changed(hass, entity_id, letni_cas)
        hass.my_log(f"---------- {date_time_obj} {letni_cas}")
        if date_time_obj is None:
            return None
        sec = time.mktime(date_time_obj.timetuple())
        return sec

    @staticmethod
    def get_changed_diff_sec(basicApp, entity_id: str) -> float:
        """Vraci rozdil v sekundach kdy byla zmena

        Args:
            entity_id (str): entita

        Returns:
            float: rozdil ve vterinach
        """
        letni_cas = basicApp.letni_cas
        ted = DateTimeOp.just_now_sec()
        last_updated = DateTimeOp.get_last_changed_sec(basicApp, entity_id, letni_cas)
        if last_updated is None:
            return 0
        return ted - last_updated

    @staticmethod
    def dif_time_sec(s_time: str, letni_cas: bool) -> float:
        """Z načteného stavu přepočte k aktuálnímu datumu vteřiny

        Args:
            s_time (str): čas zapsaný jako string
            letni_cas (bool): ano, pokud je letni cas

        Returns:
            float: [description]
        """
        ted = DateTimeOp.just_now_sec()
        date_time_obj = datetime.datetime.strptime(s_time, "%Y-%m-%dT%H:%M:%S.%f+00:00")
        date_time_obj = DateTimeOp._uprav_cas(date_time_obj, letni_cas)
        sec = time.mktime(date_time_obj.timetuple())
        return ted - sec

    @staticmethod
    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    @staticmethod
    def convert_to_datetime(tm_hour, tm_min, tm_second):
        now = DateTimeOp.just_now()
        return now.replace(hour=tm_hour, minute=tm_min, second=tm_second)

    @staticmethod
    def is_in_time_interval(
        start_hour, start_min, start_second, end_hour, end_min, end_second
    ):
        now = DateTimeOp.just_now()
        start_time = DateTimeOp.convert_to_datetime(start_hour, start_min, start_second)
        end_time = DateTimeOp.convert_to_datetime(end_hour, end_min, end_second)
        return (now >= start_time) and (now <= end_time)

    @staticmethod
    def is_in_hour_interval(start_hour: int, end_hour: int) -> bool:
        """Pokud je v daném intervalu, vrací True

        Args:
            start_hour (int): zacatek
            end_hour (int): konec

        Returns:
            bool: True, je-li v intervalu
        """
        return DateTimeOp.is_in_time_interval(start_hour, 0, 0, end_hour, 0, 0)
