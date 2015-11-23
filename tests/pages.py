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
        # self.driver.maximize_window()


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
    # SUGGEST_LIST = '.bigsearch__blocksearch__suggest'
    TITLES = '.bigsearch__blocksearch__suggest__title'
    ITEMS = '.bigsearch__blocksearch__suggest__item__title__name a'
    MAX_movies_NUMBER = 3

    def movies_titles(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.ITEMS).is_displayed()
        )
        items = self.driver.find_elements_by_css_selector(self.ITEMS)
        movies = [item.text for item in items]
        return movies[:self.MAX_movies_NUMBER]

class SearchResultPage(Component):
    ELEMENT_NUBMER_BADGES = '.countyellow'
    TERMINATOR_MOVIE_TITLE = '//a[text()="Терминатор"]'

    def movies_number(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUBMER_BADGES)
        return elements_numbers[0].text


    def series_nubmer(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUBMER_BADGES)
        return elements_numbers[1].text

    def terminator_movie_click(self):
        self.driver.find_element_by_xpath(self.TERMINATOR_MOVIE_TITLE).click()

class MoviePage(Component):
    MOVIE_TITLE_ENG = '.movieabout__nameeng'

    def movie_title_eng(self):
        title_eng = self.driver.find_element_by_css_selector(self.MOVIE_TITLE_ENG)
        return title_eng.text





