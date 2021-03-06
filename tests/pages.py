# -*- coding: utf-8 -*-
import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class Page(object):
    BASE_URL = 'https://afisha.mail.ru/'
    PATH = ''
    INPUT_FIELD = '//input[@placeholder="Введите название фильма, сериала или телешоу"]'
    AFISHA_LOGO = 'img.pm-logo__link__pic'
    WINDOW_MIN_WIDTH = 1280

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.set_window_size(self.WINDOW_MIN_WIDTH, 600)
        self.driver.maximize_window()
        self.wait_page()
        input_field = self.driver.find_element_by_xpath(self.INPUT_FIELD)
        self.driver.execute_script("return arguments[0].scrollIntoView();", input_field)

    def wait_page(self):
        wait_for_page = WebDriverWait(self.driver, 30)
        wait_for_page.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.AFISHA_LOGO))
        )


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
    def item_info(self):
        return ItemInfo(self.driver)


class SearchForm(Component):
    SEARCH_FIELD = '//input[@placeholder="Введите название фильма, сериала или телешоу"]'
    SEARCH_BUTTON = '//span[text()="Найти"]'
    SEARCH_RESULTS_PAGE_TITLE = '//h1[text()="Результаты поиска"]'
    AUTOCOMPLETE_RESULT = '.bigsearch__blocksearch__suggest__item'

    def input_query_and_wait(self, query):
        ITEM_WITH_QUERY = '//div[@class="bigsearch__blocksearch__suggest__item__title__name"]/a[text()="%s"]' % query

        self.driver.find_element_by_xpath(self.SEARCH_FIELD).send_keys(query)
        wait = WebDriverWait(self.driver, 5, 1)
        wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, ITEM_WITH_QUERY))
        )

    def input_query(self, query):
        self.driver.find_element_by_xpath(self.SEARCH_FIELD).send_keys(query)

    def submit(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, self.SEARCH_BUTTON))
        )
        self.driver.find_element_by_xpath(self.SEARCH_BUTTON).click()


class SuggestList(Component):
    SUGGEST_ITEMS  = '.bigsearch__blocksearch__suggest > div'
    CATEGORY_CLASS = 'bigsearch__blocksearch__suggest__title'
    ITEM = '.bigsearch__blocksearch__suggest__item'
    TITLE = '.bigsearch__blocksearch__suggest__item__title__name a'
    ENG_TITLE = '.bigsearch__blocksearch__suggest__item__title__eng'
    YEAR = '.bigsearch__blocksearch__suggest__item__info > *:first-child'
    COUNTRY = '.bigsearch__blocksearch__suggest__item__info > *:nth-child(3)'


    def is_present(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.ITEM))
            )
            return True
        except TimeoutException:
            return False

    def items_by_category(self, category):
        self.is_present()
        items = []
        is_category = False

        suggest_items = self.driver.find_elements_by_css_selector(self.SUGGEST_ITEMS)
        for item in suggest_items:
            if item.get_attribute('class') == self.CATEGORY_CLASS:
                is_category = item.text == category
            else:
                if is_category: items.append(item)
        return items

    def items_years_by_category(self, category):
        items = self.items_by_category(category)
        return [item.find_element_by_css_selector(self.YEAR).text for item in items]

    def items_titles_by_category(self, category):
        items = self.items_by_category(category)
        return [item.find_element_by_css_selector(self.TITLE).text for item in items]

    def items_titles(self):
        items = self.items()
        return [item.text for item in items]

    def items(self):
        self.is_present()
        return self.driver.find_elements_by_css_selector(self.TITLE)

    def first_item_by_title(self, title):
        items = self.items()
        items_with_title = [item for item in items if item.text == title]
        return None if len(items_with_title) == 0 else items_with_title[0]

    def wait_autocomplete (self):
        WebDriverWait(self.driver, 5).until(
            lambda driver :
                driver.find_elements_by_css_selector(
                    self.ITEM
                )
        )

    def find_by_selector (self, selector):
        self.wait_autocomplete()
        items = self.driver.find_elements_by_css_selector(selector)
        return [item.text for item in items]



class SearchResult(Component):
    ELEMENT_NUMBER_BADGES = '.countyellow'
    HEADER_TITLE = 'h1.title__title'
    BLOCK = '.block.block_shadow_bottom'
    BLOCK_HEADER = '.hdr__inner'
    BLOCK_ITEM_NAME = '.searchitem__item__name a'
    BLOCK_ITEM_NAME_YEAR = '.searchitem__item__name'

    def movies_number(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUMBER_BADGES)
        return elements_numbers[0].text

    def series_number(self):
        elements_numbers = self.driver.find_elements_by_css_selector(self.ELEMENT_NUMBER_BADGES)
        return elements_numbers[1].text

    def item_title(self, title):
        ITEM_TITLE = '//div[@class="searchitem__item__name"]/a[text()="%s"]' % title
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, ITEM_TITLE))
        )
        return self.driver.find_element_by_xpath(ITEM_TITLE)

    def results_title(self):
        wait_for_result_page = WebDriverWait(self.driver, 15)
        wait_for_result_page.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.HEADER_TITLE))
        )
        return self.driver.find_element_by_css_selector(self.HEADER_TITLE).text

    def result_items(self):
        return self.driver.find_elements_by_css_selector(self.BLOCK_ITEM_NAME)

    def result_years(self):
        return self.driver.find_elements_by_css_selector(self.BLOCK_ITEM_NAME_YEAR)


class ItemInfo(Component):
    ITEM_TITLE = '.movieabout__name'
    ITEM_TITLE_ENG = '.movieabout__nameeng'
    SELECTED_NAVBAR_TAB = '.pm-toolbar__group .pm-toolbar__button_current .pm-toolbar__button__text__inner_current'

    def item_title(self):
        return self.driver.find_element_by_css_selector(self.ITEM_TITLE).text

    def item_title_eng(self):
        return self.driver.find_element_by_css_selector(self.ITEM_TITLE_ENG).text

    def selected_navbar_tab_title(self):
        return self.driver.find_element_by_css_selector(self.SELECTED_NAVBAR_TAB).text