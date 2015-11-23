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

    def test_accurate_film_search(self):
        query = u'Терминатор'
        query_eng = 'The Terminator'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(query)

        suggest_list = search_page.suggestlist
        movies_titles = suggest_list.movies_titles()
        self.assertTrue(query in movies_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        movies_number = result_page.movies_number()
        self.assertEqual(int(movies_number), 9)
        series_number = result_page.series_nubmer()
        self.assertEqual(int(series_number), 1)
        result_page.terminator_movie_click()

        movie_page = MoviePage(self.driver)
        title_eng = movie_page.movie_title_eng()
        self.assertEqual(title_eng, query_eng)



    def tearDown(self):
        self.driver.quit()
