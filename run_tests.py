# -*- coding: utf-8 -*-

import sys
import unittest
from tests.test import AccurateSearchTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AccurateSearchTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
