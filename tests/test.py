# -*- coding: utf-8 -*-

import os
import unittest
import urlparse
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):
    BASE_URL = 'https://afisha.mail.ru/msk/cinema/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class SearchPage(Page):
    PATH = ''

    @property
    def searchform(self):
        return SearchForm(self.driver)

    @property
    def suggestlist(self):
        return SuggestList(self.driver)


class SearchForm(Component):
    INPUT_FIELD   = '//input[@placeholder="Введите название фильма, сериала или телешоу"]'
    SEARCH_BUTTON = '//span[text()="Найти"]'

    def input_query(self, query):
        self.driver.find_element_by_xpath(self.INPUT_FIELD).send_keys(query)

    def submit(self):
        self.driver.find_element_by_xpath(self.SEARCH_BUTTON).click()


class SuggestList(Component):
    SUGGEST_LIST = '.bigsearch__blocksearch__suggest'
    TITLES = '.bigsearch__blocksearch__suggest__title'
    ITEMS = '.bigsearch__blocksearch__suggest__item__title__name a'
    MAX_FILMS_NUMBER = 3

    def films_titles(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SUGGEST_LIST).is_displayed()
        )
        items = self.driver.find_elements_by_css_selector(self.ITEMS)
        films = [item.text for item in items]
        return films[:self.MAX_FILMS_NUMBER]


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
