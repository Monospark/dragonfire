#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#

import natlink
import threading

from dragonfly.engines.base import EngineBase
from dragonfly.engines.backend_remote.server import ServerEngine, WorkType, Action


class ClientEngine(EngineBase):

    DictationContainer = None

    def __init__(self, engine_type):
        EngineBase.__init__(self)
        self.__loaded_grammars = []
        if engine_type == "natlink":
            from dragonfly.engines.backend_natlink import get_engine
            self._wrapped_engine = get_engine()
            natlink.setTimerCallback(self.client_work, int(0.025 * 1000))
        if engine_type == "sapi5":
            from dragonfly.engines.backend_sapi5 import get_engine
            self._wrapped_engine = get_engine()
            threading.Timer(self.client_work, 0.025 * 1000).start()
        ClientEngine.DictationContainer = self._wrapped_engine.DictationContainer

    def get_grammar_by_id(self, id):
        for grammar in self.__loaded_grammars:
            if grammar.name == id:
                return grammar
        raise LookupError()

    def client_work(self):
        returned = ServerEngine.communicate(Action.FETCH_WORK)
        while returned is not Action.ACK:
            if returned == WorkType.CONNECT:
                self._wrapped_engine.connect()
            elif returned == WorkType.DISCONNECT:
                self._wrapped_engine.disconnect()
            type = returned[0]
            data = returned[1:]
            if type == WorkType.LOAD_GRAMMAR:
                grammar = data[0]
                grammar.load()
            elif type == WorkType.UNLOAD_GRAMMAR:
                grammar = self.get_grammar_by_id(data[0])
                grammar.unload()
            elif type == WorkType.ENABLE_GRAMMAR:
                grammar = self.get_grammar_by_id(data[0])
                grammar.enable()
            elif type == WorkType.DISABLE_GRAMMAR:
                grammar = self.get_grammar_by_id(data[0])
                grammar.disable()
            elif type == WorkType.UPDATE_LIST:
                grammar_id, list_id, list_data = data
                grammar = self.get_grammar_by_id(grammar_id)

                def get_list_by_id(grammar, id):
                    for list in grammar._lists:
                        if list.id == id:
                            return list
                    raise LookupError()
                list = get_list_by_id(grammar, list_id)
                list.set(list_data)
            returned = ServerEngine.communicate(Action.FETCH_WORK)

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def _load_grammar(self, grammar):
        self._wrapped_engine.load_grammar(grammar)
        self.__loaded_grammars.append(grammar)

    def _unload_grammar(self, grammar, wrapper):
        self._wrapped_engine.unload_grammar(grammar, wrapper)
        self.__loaded_grammars.remove(grammar)

    def update_list(self, lst, grammar):
        # TODO
        self._wrapped_engine.update_list(lst, grammar)

    def activate_grammar(self, grammar):
        # TODO
        self._wrapped_engine.activate_grammar(grammar)

    def deactivate_grammar(self, grammar):
        # TODO
        self._wrapped_engine.deactivate_grammar(grammar)

    def mimic(self, words):
        raise NotImplementedError()

    def speak(self, text):
        raise NotImplementedError()

    def _get_language(self):
        return self._wrapped_engine._get_language()
