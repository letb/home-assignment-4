# -*- coding: utf-8 -*-

import sys
import unittest
from tests.test import AccurateSearchTest, SymbolsSearchTest, EmptySearchTest, NonExistentSearchTest
from tests.test import LongQuerySearchTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AccurateSearchTest),
        unittest.makeSuite(SymbolsSearchTest),
        unittest.makeSuite(EmptySearchTest),
        unittest.makeSuite(NonExistentSearchTest),
        unittest.makeSuite(LongQuerySearchTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
