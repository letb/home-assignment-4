# -*- coding: utf-8 -*-

import os
import unittest
import urlparse
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait

from pages import *


class AccurateSearchTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_accurate_movie_search(self):
        TITLE = u'Терминатор'
        TITLE_ENG = 'The Terminator'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(TITLE)

        suggest_list = search_page.suggestlist
        movies_titles = suggest_list.items_titles()
        self.assertTrue(TITLE in movies_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result

        movies_number = search_result.movies_number()
        self.assertEqual(int(movies_number), 9)
        series_number = search_result.series_number()
        self.assertEqual(int(series_number), 1)
        search_result.item_title(TITLE).click()

        movie_page = ItemPage(self.driver)
        movie_info = movie_page.movie_info
        title_eng = movie_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def test_accurate_series_search(self):
        QUERY = u'Пайтон'
        TITLE = u'Летающий цирк Монти Пайтона'
        TITLE_ENG = 'Monty Python\'s Flying Circus'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)

        suggest_list = search_page.suggestlist
        series_titles = suggest_list.items_titles()
        self.assertTrue(TITLE in series_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        search_result.item_title(TITLE).click()

        series_page = ItemPage(self.driver)
        movie_info = series_page.movie_info
        title_eng = movie_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def tearDown(self):
        self.driver.quit()
