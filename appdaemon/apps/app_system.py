from base_op import BaseOp
from globals import SENSOR_MODULE_ENTITES, ON
import yaml
import io
import os
import re
import ntpath
import global_app_system as gas
from helper_tools import MyHelp as h
from globals_def import eventsDef as e


class AppSystem(BaseOp):
    """Control of creating user defined entities
    Reading from api.yaml all globals and searching @auto_create and @end
    fire e.ENTITIES_CREATED to allow listening - entities defined

    Args:
        BasicApp ([type]): root class
    """

    def initialize(self):
        # There is defined call of entities_defined
        super().initialize()
        # Pokud jiz existuje SENSOR_MODULE_ENTITES, je potreba ho vyzkouset, pokud vubec funguje
        if self.entity_exists(SENSOR_MODULE_ENTITES):
            self.set_entity_state(SENSOR_MODULE_ENTITES, False)
        self.log_button = "input_boolean.log_app_system"
        self.defined_entities: list = []
        self.after_at = "#\s*(.*)"
        self.listen_event(self._check, e.DEFINE_ENTITIES)
        self.run_in(self._wait_module_entities, 1)

    def _wait_module_entities(self, *kwargs):
        # Nejprve musi byt zadefinovan SENSOR_MODULE_ENTITES
        # Tzn. lze tvorit entity
        # Na zacatku byl nastaven na OFF inicializaci
        # Nyni bude fire do te doby nez bude ON
        self.fire_event(e.SENSOR_MODULE_ENTITIES_ON)
        self.my_log("Wait")

        self.my_log(f"Wait for module entities {SENSOR_MODULE_ENTITES}")
        if self.entity_exists(SENSOR_MODULE_ENTITES):
            if self.get_state(SENSOR_MODULE_ENTITES) == ON:
                self.my_log("Going to define")
                self.run_in(self._check, 1)
                return
        self.run_in(self._wait_module_entities, 1)

    def parse(self, filename: str, pattern_def: tuple):
        lines: list = []
        with open(filename) as f:
            lines = f.readlines()
        start_block = False

        for line in lines:
            self.my_log(f"{start_block} Line: {line}")
            if start_block:
                if "@end" in line:
                    start_block = False
            if start_block:
                for pattern in pattern_def:
                    found = re.search(pattern, line)
                    if found:
                        entity = found.group(0)[1:-1]
                        if not h.in_array(entity, gas.defined_entities):
                            gas.defined_entities.append(entity)
                            self.my_log(f"Pridavam: {entity}")
                        if self.entity_exists(entity):
                            continue
                        attr = {}
                        found = re.search(self.after_at, line)
                        if found:
                            after_at = found.group(0)[1:].strip()
                            attr = eval(after_at)
                        self.defined_entities.append((entity, attr))
            if not start_block:
                start_block = "@auto_create" in line

    def _check(self, *kwargs):
        self.my_log("Check")
        global_list = ("global_app_system", "global_indego")
        file_path = os.path.realpath(__file__)
        path = ntpath.dirname(file_path) + "/"
        with open(f"{path}apps.yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)
        glob = data_loaded["global_modules"]
        for f in glob:
            if not f in global_list:
                continue
            filename = path + f + ".py"
            if os.path.exists(filename):
                types = (
                    "input_boolean",
                    "input_number",
                    "input_text",
                    "sensor",
                    "binary_sensor",
                )
                patterns: list = []
                for t in types:
                    patterns.append('"' + t + '.(.+?)"')
                self.parse(filename, patterns)
            else:
                self.my_log(f"----Vymazat: {filename}")
        for ib in self.defined_entities:
            self.my_log(ib)
            self.create_entity(ib[0], attributes=ib[1])
        self.run_in(self._kontrola_vytvoreni, 1)

    def _system_ready(self, value):
        if self.entity_exists(gas.SYSTEM_READY):
            self.set_entity_state(gas.SYSTEM_READY, value)

    def _kontrola_vytvoreni(self, *kwargs):
        self.my_log("kontrola")
        repeat = True
        watchdog = 10
        while repeat and watchdog > 0:
            watchdog -= 1
            self.my_log("Tocim")
            repeat = False

            for ib in self.defined_entities:
                if not self.entity_exists(ib[0]):
                    self.my_log(f"{watchdog} neexistuje!: {ib[0]}")
                    repeat = True
        self.listen_on(self._check, gas.CHECK_API)
        self._system_ready(True)
