# -*- coding: utf-8 -*-

import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from pages import SearchPage, SearchResultPage, ItemPage


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
        movie_info = movie_page.item_info
        title_eng = movie_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def test_accurate_series_search(self):
        QUERY = u'Летающий цирк Монти Пайтона'
        TITLE = u'Летающий цирк Монти Пайтона'
        TITLE_ENG = 'Monty Python\'s Flying Circus'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)

        suggest_list = search_page.suggestlist
        suggested_titles = suggest_list.items_titles()
        self.assertIn(TITLE, suggested_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        search_result.item_title(TITLE).click()

        series_page = ItemPage(self.driver)
        series_info = series_page.item_info
        title_eng = series_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def test_accurate_show_search(self):
        QUERY = u'Хочу к Меладзе'
        TITLE = u'Хочу к Меладзе'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)

        suggest_list = search_page.suggestlist
        suggested_titles = suggest_list.items_titles()
        self.assertIn(TITLE, suggested_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        search_result.item_title(TITLE).click()

        show_page = ItemPage(self.driver)
        show_info = show_page.movie_info
        # todo: assert menubar on tvshow

    def tearDown(self):
        self.driver.quit()


class SymbolsSearchTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_search_numbers(self):
        QUERY = '300'
        TITLE = u'300 спартанцев'
        TITLE_ENG = '300'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        item_title = search_result.item_title(TITLE)
        self.assertEqual(item_title.text, TITLE)
        item_title.click()

        movie_page = ItemPage(self.driver)
        movie_info = movie_page.item_info
        title_eng = movie_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def test_search_symbols(self):
        QUERY = '1+1'
        TITLE = '1+1'
        TITLE_ENG = 'Intouchables'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        item_title = search_result.item_title(TITLE)
        self.assertEqual(item_title.text, TITLE)
        item_title.click()

        movie_page = ItemPage(self.driver)
        movie_info = movie_page.item_info
        title_eng = movie_info.item_title_eng()
        self.assertEqual(title_eng, TITLE_ENG)

    def tearDown(self):
        self.driver.quit()


class EmptySearchTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_empty_search(self):
        QUERY = ''

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        result_items = search_result.result_items()
        self.assertFalse(result_items)

    def tearDown(self):
        self.driver.quit()


class NonExistentSearchTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_non_existent_search(self):
        QUERY = 'NON-EXISTENT MOVIE'

        search_page = SearchPage(self.driver)
        search_page.open()

        search_form = search_page.searchform
        search_form.input_query(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        result_items = search_result.result_items()
        self.assertFalse(result_items)

    def tearDown(self):
        self.driver.quit()
