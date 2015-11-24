# -*- coding: utf-8 -*-

import os
import unittest
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote

from pages import SearchPage, SearchResultPage, ItemPage


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class BaseTestCase(unittest.TestCase):
    search_page = None

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.search_page = SearchPage(self.driver)
        self.search_page.open()
        # browser = os.environ.get('TTHA2BROWSER', 'CHROME')
        #
        # self.driver = Remote(
        #     command_executor='http://127.0.0.1:4444/wd/hub',
        #     desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        # )

    def tearDown(self):
        self.driver.quit()


class AccurateSearchTest(BaseTestCase):
    def test_accurate_movie_search(self):
        TITLE = u'Терминатор'
        TITLE_ENG = 'The Terminator'

        search_form = self.search_page.searchform
        search_form.input_query_paste(TITLE)

        suggest_list = self.search_page.suggestlist
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
        selected_navbar_tab_title = movie_info.selected_navbar_tab_title()
        self.assertEqual(selected_navbar_tab_title, u'Кино')

    def test_accurate_series_search(self):
        QUERY = u'Летающий цирк Монти Пайтона'
        TITLE = u'Летающий цирк Монти Пайтона'
        TITLE_ENG = 'Monty Python\'s Flying Circus'

        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)

        suggest_list = self.search_page.suggestlist
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
        selected_navbar_tab_title = series_info.selected_navbar_tab_title()
        self.assertEqual(selected_navbar_tab_title, u'Сериалы')

    def test_accurate_show_search(self):
        QUERY = u'Хочу к Меладзе'
        TITLE = u'Хочу к Меладзе'

        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)

        suggest_list = self.search_page.suggestlist
        suggested_titles = suggest_list.items_titles()
        self.assertIn(TITLE, suggested_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        search_result.item_title(TITLE).click()

        show_page = ItemPage(self.driver)
        show_info = show_page.item_info
        selected_navbar_tab_title = show_info.selected_navbar_tab_title()
        self.assertEqual(selected_navbar_tab_title, u'Телешоу')


class SymbolsSearchTest(BaseTestCase):
    def symbol_search_helper(self, QUERY, TITLE, TITLE_ENG):
        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)
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

    def test_search_numbers(self):
        QUERY = '300'
        TITLE = u'300 спартанцев'
        TITLE_ENG = '300'
        self.symbol_search_helper(QUERY, TITLE, TITLE_ENG)

    def test_search_symbols(self):
        QUERY = '1+1'
        TITLE = '1+1'
        TITLE_ENG = 'Intouchables'
        self.symbol_search_helper(QUERY, TITLE, TITLE_ENG)


class VulnerableSearchTest(BaseTestCase):
    def vulnerable_search_helper(self, QUERY, control=False):

        search_form = self.search_page.searchform
        if control:
            search_form.input_query(QUERY)
        elif QUERY != '':
            search_form.input_query_paste(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        header_title = search_result.results_title()
        self.assertEqual(header_title, u'Результаты поиска')
        result_items = search_result.result_items()
        self.assertFalse(result_items)

    def test_empty_search(self):
        QUERY = ''
        self.vulnerable_search_helper(QUERY)

    def test_long_query_search(self):
        QUERY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        self.vulnerable_search_helper(QUERY)

    def test_control_characters_search(self):
        QUERY = '\\0\\a \\b \\t \\n \\v \\f \\r'
        control = True
        self.vulnerable_search_helper(QUERY, control)


class NonExistentSearchTest(BaseTestCase):
    def test_non_existent_search(self):
        QUERY = 'NON-EXISTENT MOVIE'

        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        header_title = search_result.results_title()
        self.assertEqual(header_title, u'Результаты поиска')
        result_items = search_result.result_items()
        self.assertFalse(result_items)


class YearQuerySearchTest(BaseTestCase):
    def test_not_search_by_year_in_query(self):
        QUERY = "2010"

        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        header_title = search_result.results_title()
        self.assertEqual(header_title, u'Результаты поиска')
        result_items = search_result.result_years()
        first_movie_year = result_items[0].text[-6:][1:5]
        self.assertNotEqual(int(first_movie_year), 2010)


# 1.2.1 Работает контекстная подсказка
class SuggesterTest(BaseTestCase):
    def test_suggester_works(self):
        QUERY = u'Марина'
        search_form = self.search_page.searchform
        search_form.input_query_paste(QUERY)

        suggest_list = self.search_page.suggestlist
        self.assertTrue(suggest_list.is_present())

        items_titles = suggest_list.items_titles()
        self.assertIn(QUERY, items_titles)
        item_with_title = suggest_list.first_item_by_title(QUERY)
        self.assertIsNotNone(item_with_title)

        item_with_title.click()
        item_page = ItemPage(self.driver)
        item_info = item_page.item_info
        title = item_info.item_title()
        self.assertEqual(title, QUERY)


# 1.2.2 Элементы в подсказке разбиваются по соответствующим категориям:
class SuggestCategoryTest(BaseTestCase):
    def display_suggest_list(self, query):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)
        return self.search_page.suggestlist

    # 1.2.2.1 Фильм отображается в подсказке, если такой есть
    def test_suggest_film(self):
        QUERY = u'Персона'
        CATEGORY = u'ФИЛЬМЫ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.2 Сериал отображается в подсказке, если такой есть
    def test_suggest_series(self):
        QUERY = u'Теория большого взрыва'
        CATEGORY = u'СЕРИАЛЫ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.3 Телешоу отображается в подсказке, если такое есть
    def test_suggest_show(self):
        QUERY = u'Битва экстрасенсов'
        CATEGORY = u'ТЕЛЕШОУ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.4 Персона отображается в подсказке, если есть совпадение с именем
    def test_suggest_person(self):
        QUERY = u'Кристиан Бэйл'
        CATEGORY = u'ПЕРСОНЫ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.5 Новость отображается в подсказке, если есть совпадение с заголовком
    def test_suggest_news(self):
        QUERY = u'Голубой мет из сериала «Во все тяжкие» подарили музею США'
        CATEGORY = u'НОВОСТИ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.6 Подборка отображается в подсказке, если есть совпадение с заголовком
    def test_suggest_selection(self):
        QUERY = u'10 самых ожидаемых фильмов ноября'
        CATEGORY = u'ПОДБОРКИ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.7 Место отображается в подсказке, если есть совпадение с заголовком
    def test_suggest_place(self):
        QUERY = u'Большой театр'
        CATEGORY = u'МЕСТА'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))

    # 1.2.2.8 Событие отображается в подсказке, если есть совпадение с заголовком
    def test_suggest_event(self):
        QUERY = u'Свадьба Фигаро'
        CATEGORY = u'СОБЫТИЯ'

        suggest_list = self.display_suggest_list(QUERY)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(QUERY, suggest_list.items_titles_by_category(CATEGORY))


class CorrectDisplayTest(BaseTestCase):

    base_query = u'День'

    def starts_with_year(self, str, splitter):
        return represents_int(str.split(splitter)[0])

    def display_search_helper(self, query, selector):
        search_form = self.search_page.searchform
        search_form.input_query(query)

        suggest_list = self.search_page.suggestlist
        items = suggest_list.find_by_selector(selector)

        return items

    def test_display_years(self):
        years = self.display_search_helper(self.base_query, self.search_page.suggestlist.YEARS)
        self.assertEqual(years.__len__(), 7)

    def test_display_titles(self):
        titles = self.display_search_helper(self.base_query, self.search_page.suggestlist.TITLES)
        self.assertEqual(titles.__len__(), 7)

    def test_display_countries(self):
        countries = self.display_search_helper(self.base_query, self.search_page.suggestlist.COUNTRIES)
        self.assertEqual(countries.__len__(), 7)

    def test_display_english_titles(self):
        QUERY = u'При'
        items = self.display_search_helper(QUERY, self.search_page.suggestlist.ITEMS)

        for i, val in enumerate(items):
            country_list = val.split('/')[1]
            main_country = country_list.split(',')[0]
            headers_array = val.split('\n')
            if main_country == u'Россия':
                self.assertTrue(self.starts_with_year(headers_array[1], '/'))
            else:
                self.assertFalse(self.starts_with_year(headers_array[1], '/'))


class EmptySuggestTest(BaseTestCase):

    def display_search_helper(self, query):
        search_form = self.search_page.searchform
        search_form.input_query(query)

        suggest_list = self.search_page.suggestlist
        return suggest_list.find_by_selector(suggest_list.CATEGORY_CLASS)

    def test_display_years(self):
        QUERY = u'Буллшит'
        items = self.display_search_helper(QUERY)
        self.assertEqual(items.__len__(), 0)
