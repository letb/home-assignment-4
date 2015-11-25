# -*- coding: utf-8 -*-

import sys
import unittest

from tests.test import AccurateSearchTest, SymbolsSearchTest, \
                       NonExistentSearchTest, VulnerableSearchTest, \
                       YearQuerySearchTest, CorrectDisplayTest, \
                       SuggesterTest, SuggestCategoryTest, \
                       EmptySuggestTest, YearQuerySuggestTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AccurateSearchTest),
        unittest.makeSuite(SymbolsSearchTest),
        unittest.makeSuite(NonExistentSearchTest),
        unittest.makeSuite(VulnerableSearchTest),
        unittest.makeSuite(YearQuerySearchTest),
        unittest.makeSuite(CorrectDisplayTest),
        unittest.makeSuite(SuggesterTest),
        unittest.makeSuite(SuggestCategoryTest),
        unittest.makeSuite(EmptySuggestTest),
        unittest.makeSuite(YearQuerySuggestTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
