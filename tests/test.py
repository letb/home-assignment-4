# -*- coding: utf-8 -*-

import os
import unittest

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
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        self.search_page = SearchPage(self.driver)
        self.search_page.open()

    def tearDown(self):
        self.driver.quit()


class AccurateSearchTest(BaseTestCase):
    def accurate_search_helper(self, query, title, category):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)

        suggest_list = self.search_page.suggestlist
        suggested_titles = suggest_list.items_titles()
        self.assertIn(title, suggested_titles)

        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        search_result.item_title(title).click()

        item_page = ItemPage(self.driver)
        item_info = item_page.item_info
        selected_navbar_tab_title = item_info.selected_navbar_tab_title()
        self.assertEqual(selected_navbar_tab_title, category)


    def test_accurate_movie_search(self):
        QUERY = u'Терминатор'
        TITLE = u'Терминатор'
        CATEGORY = u'Кино'

        self.accurate_search_helper(QUERY, TITLE, CATEGORY)

    def test_accurate_series_search(self):
        QUERY = u'Летающий цирк Монти Пайтона'
        TITLE = u'Летающий цирк Монти Пайтона'
        CATEGORY = u'Сериалы'

        self.accurate_search_helper(QUERY, TITLE, CATEGORY)

    def test_accurate_show_search(self):
        QUERY = u'Хочу к Меладзе'
        TITLE = u'Хочу к Меладзе'
        CATEGORY = u'Телешоу'

        self.accurate_search_helper(QUERY, TITLE, CATEGORY)


class SymbolsSearchTest(BaseTestCase):
    def symbol_search_helper(self, query, title, title_eng):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)
        search_form.submit()

        result_page = SearchResultPage(self.driver)
        search_result = result_page.search_result
        item_title = search_result.item_title(title)
        self.assertEqual(item_title.text, title)
        item_title.click()

        movie_page = ItemPage(self.driver)
        movie_info = movie_page.item_info
        item_title_eng = movie_info.item_title_eng()
        self.assertEqual(item_title_eng, title_eng)

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
    def vulnerable_search_helper(self, query, control=False):
        search_form = self.search_page.searchform
        if control:
            search_form.input_query(query)
        elif query != '':
            search_form.input_query_paste(query)
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


class SuggestCategoryTest(BaseTestCase):
    def display_suggest_list(self, query):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)

        return self.search_page.suggestlist

    def suggest_category_helper(self, query, category):
        suggest_list = self.display_suggest_list(query)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(query, suggest_list.items_titles_by_category(category))

    def test_suggest_film(self):
        QUERY = u'Персона'
        CATEGORY = u'ФИЛЬМЫ'
        self.suggest_category_helper(QUERY, CATEGORY)

    def test_suggest_series(self):
        QUERY = u'Теория большого взрыва'
        CATEGORY = u'СЕРИАЛЫ'
        self.suggest_category_helper(QUERY, CATEGORY)

    def test_suggest_show(self):
        QUERY = u'Битва экстрасенсов'
        CATEGORY = u'ТЕЛЕШОУ'
        self.suggest_category_helper(QUERY, CATEGORY)

    def test_suggest_person(self):
        QUERY = u'Кристиан Бэйл'
        CATEGORY = u'ПЕРСОНЫ'
        self.suggest_category_helper(QUERY, CATEGORY)

    def test_suggest_news(self):
        QUERY = u'Голубой мет из сериала «Во все тяжкие» подарили музею США'
        CATEGORY = u'НОВОСТИ'
        self.suggest_category_helper(QUERY, CATEGORY)

    def test_suggest_selection(self):
        QUERY = u'10 самых ожидаемых фильмов ноября'
        CATEGORY = u'ПОДБОРКИ'
        self.suggest_category_helper(QUERY, CATEGORY)


    def test_suggest_place(self):
        QUERY = u'Большой театр'
        CATEGORY = u'МЕСТА'
        self.suggest_category_helper(QUERY, CATEGORY)


    def test_suggest_event(self):
        QUERY = u'Свадьба Фигаро'
        CATEGORY = u'СОБЫТИЯ'
        self.suggest_category_helper(QUERY, CATEGORY)


class YearQuerySuggestTest(BaseTestCase):
    def display_suggest_list(self, query):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)
        return self.search_page.suggestlist

    def year_query_suggest_helper(self, query, category):
        suggest_list = self.display_suggest_list(query)
        self.assertTrue(suggest_list.is_present())
        self.assertIn(query, suggest_list.items_years_by_category(category))

    def test_suggest_film_by_year(self):
        QUERY = '2012'
        CATEGORY = u'СЕРИАЛЫ'
        self.year_query_suggest_helper(QUERY, CATEGORY)

    def test_suggest_show_by_year(self):
        QUERY = '2012'
        CATEGORY = u'ТЕЛЕШОУ'
        self.year_query_suggest_helper(QUERY, CATEGORY)
#


class CorrectDisplayTest(BaseTestCase):
    base_query = u'День'
    results_array = [
        u'Приключения Маши в Стране Чудес\nYugo and Lala\n2012/Китай',
        u'Притяжение\n2017/Россия',
        u'Пристанище\nLura\n2013/Португалия',
        u'Присоска\nSuckers\n2009/США, Испания',
        u'Принцесса Фантагира\nFantaghiro\n1999/Испания',
        u'Принцесса и нищенка\n2009/Россия',
        u'Слава богу, ты пришёл!\n2006/Россия',
    ]

    def starts_with_year(self, str, splitter):
        return represents_int(str.split(splitter)[0])

    def display_search_helper(self, query, selector):
        search_form = self.search_page.searchform
        search_form.input_query_paste(query)

        suggest_list = self.search_page.suggestlist
        items = suggest_list.find_by_selector(selector)
        return items

    # У элемента выпадающего списка отображается год создания
    def test_display_years(self):
        years = self.display_search_helper(self.base_query, self.search_page.suggestlist.YEAR)
        self.assertEqual(len(years), 7)

    # У элемента выпадающего списка отображается страна создания
    def test_display_countries(self):
        countries = self.display_search_helper(self.base_query, self.search_page.suggestlist.COUNTRY)
        self.assertEqual(len(countries), 7)

    # У элемента выпадающего списка отображается название
    # Если страна - Россия, то нет оригинального названия (есть только одно название)
    def test_display_titles(self):
        titles = self.display_search_helper(self.base_query, self.search_page.suggestlist.TITLE)
        self.assertEqual(len(titles), 7)

    # Если страна - не Россия, то есть оригинальное название
    def test_display_english_titles(self):
        QUERY = u'При'
        items = self.display_search_helper(QUERY, self.search_page.suggestlist.ITEM)

        for i, val in enumerate(items):
            self.assertTrue(val == self.results_array[i])


class EmptySuggestTest(BaseTestCase):
    def display_search_helper(self, query):
        search_form = self.search_page.searchform
        search_form.input_query(query)

        suggest_list = self.search_page.suggestlist
        return suggest_list.find_by_selector(suggest_list.CATEGORY_CLASS)

    def test_display_years(self):
        QUERY = u'Буллшит'
        items = self.display_search_helper(QUERY)
        self.assertEqual(len(items), 0)
