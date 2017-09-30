import sys
sys.path.pop(0)

import nose
from dragonfire.engines.backend_natlink import test_dictation
from dragonfire import *

if __name__ == "__main__":
    engine = get_engine()
    engine.connect()
    try:
        loader = nose.loader.TestLoader()
        suite = loader.loadTestsFromTestCase(test_dictation.EnglishNatlinkDictationTestCase)
        nose.core.TestProgram(suite=suite)
    finally:
        engine.disconnect()
