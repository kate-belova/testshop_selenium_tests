import allure
import pytest

# fmt: off
from test_data import (
    search_words, sort_indexes, sort_verifications, price_test_data
)
# fmt: on


@pytest.mark.desks
@pytest.mark.regression
class TestDesksPage:

    @allure.feature('Categories')
    @allure.story('Desks category')
    @allure.title('Successful search by key words in Desks category')
    @pytest.mark.smoke
    @pytest.mark.parametrize('search_word', search_words)
    def test_desks_search_success(self, desks_page, search_word):
        desks_page.open_desks_page()
        desks_page.enter_search_word(search_word)
        desks_page.assert_actual_desks_count_equals_the_one_in_counter()
        desks_page.assert_search_word_in_found_products_titles(search_word)

    @allure.feature('Categories')
    @allure.story('Desks category')
    @allure.title('Successfully filter by price')
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        'min_price, max_price, expected_count', price_test_data
    )
    def test_filter_desks_by_price_range(
        self, desks_page, min_price, max_price, expected_count
    ):
        desks_page.open_desks_page()
        desks_page.change_slider_price_range(
            min_price=min_price, max_price=max_price
        )
        desks_page.assert_found_desks_count(expected_count)

    @allure.feature('Categories')
    @allure.story('Desks category')
    @allure.title('Sort desks by title a-z, price low to high and vice versa')
    @pytest.mark.parametrize('index', sort_indexes)
    def test_sort_desks(self, desks_page, index):
        desks_page.open_desks_page()
        selected_option = desks_page.select_sort_option(index)

        verification_method_name = sort_verifications[selected_option]
        verification_method = getattr(desks_page, verification_method_name)
        verification_method()

        allure.dynamic.title(f'Sort desks - {selected_option}')
