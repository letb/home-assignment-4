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
        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(query)

        suggest_list = search_page.suggestlist
        films_titles = suggest_list.films_titles()
        for film in films_titles: print film
        self.assertTrue(query in films_titles)

        search_form.submit()

    def tearDown(self):
        self.driver.quit()
