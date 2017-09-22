import socket
import sys
import threading
import time
from multiprocessing import connection
from multiprocessing.connection import Listener, Client

import __builtin__
from dragonfly.grammar.grammar_base import Grammar
from dragonfly.engines.backend_remote import remote
from dragonfly.engines.base import EngineBase

TIMEOUT = 0.5
connection._init_timeout = lambda: time.time() + TIMEOUT
ADDRESS = ('localhost', 6000)

class Action:
    ACK = 1
    GET_ENGINE = 5
    WRITE_OUTPUT = 6
    WRITE_ERROR = 7
    RULE_PROCESS_RECOGNITION = 8
    FETCH_WORK = 10


class ServerEngineType:
    NONE = 0
    NATLINK = 1
    SAPI5 = 2


class WorkType:
    CONNECT = 1
    DISCONNECT = 2
    LOAD_GRAMMAR = 3
    ENABLE_GRAMMAR = 4
    DISABLE_GRAMMAR = 5
    UNLOAD_GRAMMAR = 6
    UPDATE_LIST = 7



class ServerEngine(EngineBase):

    @staticmethod
    def communicate(data):
        conn = Client(ADDRESS)
        conn.send(data)
        received = conn.recv()
        return received

    @staticmethod
    def get_server_engine():
        try:
            return ServerEngine.communicate(Action.GET_ENGINE)
        except socket.error:
            return ServerEngineType.NONE

    def __init__(self, type):
        EngineBase.__init__(self)
        self.__type = type
        self._queue = []
        self.listener = Listener(ADDRESS)
        self.listener._listener._socket.settimeout(TIMEOUT)
        self._running = True
        threading.Thread(target=self.loop).start()

    def loop(self):
        while self._running:
            try:
                conn = self.listener.accept()
            except socket.timeout:
                continue
            except socket.error:
                break
            else:
                self.handle_connection(conn)
        self.listener.close()

    def stop(self):
        self._running = False

    def handle_connection(self, conn):
        msg = conn.recv()
        action_answer = self.handle_action(msg)
        if action_answer is not None:
            try:
                conn.send(action_answer)
            except Exception as e:
                def a(e):
                    for v in e.__dict__:
                        print type(v)
                        if isinstance(v, function):
                            pass
                        else:
                            a(v)
                a(action_answer)
        else:
            data_answer = self.handle_data(msg)
            if data_answer:
                conn.send(data_answer)

    def handle_action(self, message):
        if message == Action.FETCH_WORK:
            if len(self._queue) == 0:
                return Action.ACK
            else:
                value = self._queue[0]
                self._queue.remove(value)
                return value
        if message == Action.GET_ENGINE:
            return self.__type
        return None

    def handle_data(self, message):
        action, data = message
        if action == Action.RULE_PROCESS_RECOGNITION:
            id, node = data
            remote.process_recognition(id, node)
            return Action.ACK
        if action == Action.WRITE_OUTPUT:
            sys.stdout.write(data)
            return Action.ACK
        if action == Action.WRITE_ERROR:
            sys.stderr.write(data)
            return Action.ACK
        return None

    def connect(self):
        self._queue.append(WorkType.CONNECT)

    def disconnect(self):
        self._queue.append(WorkType.DISCONNECT)

    def _load_grammar(self, grammar):
        self._queue.append((WorkType.LOAD_GRAMMAR, remote.create_remote_grammar(grammar)))

    def _unload_grammar(self, grammar, wrapper):
        self._queue.append((WorkType.UNLOAD_GRAMMAR, remote.get_remote_grammar_id(grammar)))

    def on_grammar_enable(self, grammar):
        self._queue.append((WorkType.ENABLE_GRAMMAR, remote.get_remote_grammar_id(grammar)))

    def on_grammar_disable(self, grammar):
        self._queue.append((WorkType.DISABLE_GRAMMAR, remote.get_remote_grammar_id(grammar)))

    def update_list(self, list, grammar):
        if isinstance(list, __builtin__.list):
            data = __builtin__.list(list)
        else:
            data = dict(list)
        self._queue.append((WorkType.UPDATE_LIST, remote.get_remote_grammar_id(grammar), remote.get_remote_list_id(list), data))

    def mimic(self, words):
        raise NotImplementedError()

    def speak(self, text):
        raise NotImplementedError()

    def _get_language(self):
        return "en"
