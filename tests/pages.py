# -*- coding: utf-8 -*-

import os
import unittest
import urlparse
import time

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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


class SearchResultPage(Page):
    PATH = ''

    @property
    def search_result(self):
        return SearchResult(self.driver)


class ItemPage(Page):
    PATH = ''

    @property
    def movie_info(self):
        return ItemInfo(self.driver)


class SearchForm(Component):
    INPUT_FIELD = '//input[@placeholder="Введите название фильма, сериала или телешоу"]'
    SEARCH_BUTTON = '//span[text()="Найти"]'

    def input_query(self, query):
        self.driver.find_element_by_xpath(self.INPUT_FIELD).send_keys(query)

    def submit(self):
        self.driver.find_element_by_xpath(self.SEARCH_BUTTON).click()


class SuggestList(Component):
    ITEMS = '.bigsearch__blocksearch__suggest__item'
    TITLES = '.bigsearch__blocksearch__suggest__item__title__name a'

    def items_titles(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.ITEMS))
        )
        items = self.driver.find_elements_by_css_selector(self.TITLES)
        titles = [item.text for item in items]
        return titles


class SearchResult(Component):
    ELEMENT_NUMBER_BADGES = '.countyellow'
    BLOCK = '.block.block_shadow_bottom'
    BLOCK_HEADER = '.hdr__inner'
    BLOCK_ITEM_NAMES = '.searchitem__item__name a'

    def movies_number(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUMBER_BADGES)
        return elements_numbers[0].text

    def series_number(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUMBER_BADGES)
        return elements_numbers[1].text

    def item_title(self, title):
        ITEM_TITLE = '//div[@class="searchitem__item__name"]/a[text()="%s"]' % title
        return self.driver.find_element_by_xpath(ITEM_TITLE)


class ItemInfo(Component):
    ITEM_TITLE_ENG = '.movieabout__nameeng'

    def item_title_eng(self):
        title_eng = self.driver.find_element_by_css_selector(self.ITEM_TITLE_ENG)
        return title_eng.text