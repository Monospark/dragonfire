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

import unittest
import dragonfire


#===========================================================================

class EngineTestSuite(unittest.TestSuite):

    def __init__(self, name):
        self.engine_name = name
        unittest.TestSuite.__init__(self)

    def run(self, result):
        engine = dragonfire.get_engine(self.engine_name)
        engine.connect()
        try:
            return unittest.TestSuite.run(self, result)
        finally:
            engine.disconnect()
