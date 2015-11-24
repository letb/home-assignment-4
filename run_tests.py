# -*- coding: utf-8 -*-

import sys
import unittest
from tests.test import AccurateSearchTest, SymbolsSearchTest, NonExistentSearchTest
from tests.test import VulnerableSearchTest, YearQuerySearchTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AccurateSearchTest),
        # unittest.makeSuite(SymbolsSearchTest),
        # unittest.makeSuite(NonExistentSearchTest),
        # unittest.makeSuite(VulnerableSearchTest),
        # unittest.makeSuite(YearQuerySearchTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
