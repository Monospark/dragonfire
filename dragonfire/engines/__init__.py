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

"""
Main SR engine back-end interface
============================================================================

"""

import logging
import traceback

from .base import EngineBase, EngineError, MimicFailure


engine_name = None
_default_engine = None


def start_server():
    global _default_engine
    from dragonfire.engines.backend_remote.server import ServerEngine, ServerEngineType
    _default_engine = ServerEngine(ServerEngineType.NATLINK)


def get_engine():
    global _default_engine
    log = logging.getLogger("engine")

    if _default_engine:
        return _default_engine

    if not engine_name:
        from dragonfire.engines.backend_remote.client import ClientEngine
        from dragonfire.engines.backend_remote.server import ServerEngine, ServerEngineType
        server_type = ServerEngine.get_server_engine()
        if server_type == ServerEngineType.NATLINK:
            _default_engine = ClientEngine("natlink")
            return _default_engine
        elif server_type == ServerEngineType.SAPI5:
            _default_engine = ClientEngine("sapi5")
            return _default_engine

    if not engine_name or engine_name == "natlink":
        # Attempt to retrieve the natlink back-end.
        try:
            from .backend_natlink import is_engine_available
            from .backend_natlink import get_engine as get_specific_engine
            if is_engine_available():
                _default_engine = get_specific_engine()
                return _default_engine
        except Exception, e:
            message = ("Exception while initializing natlink engine:"
                       " %s" % (e,))
            log.exception(message)
            traceback.print_exc()
            print message
            if engine_name:
                raise EngineError(message)

    if not engine_name or engine_name == "sapi5":
        # Attempt to retrieve the sapi5 back-end.
        try:
            from .backend_sapi5 import is_engine_available
            from .backend_sapi5 import get_engine as get_specific_engine
            if is_engine_available():
                _default_engine = get_specific_engine()
                return _default_engine
        except Exception, e:
            message = ("Exception while initializing sapi5 engine:"
                       " %s" % (e,))
            log.exception(message)
            traceback.print_exc()
            print message
            if engine_name:
                raise EngineError(message)

    if not engine_name:
        raise EngineError("No usable engines found.")
    else:
        raise EngineError("Requested engine %r not available." % (engine_name,))
