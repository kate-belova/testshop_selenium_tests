import allure
import pytest

# fmt: off
from test_data import (
    products_test_data, product_index, search_words, products_indexes
)
# fmt: on


@pytest.mark.product_page
@pytest.mark.regression
class TestProductPage:
    @allure.feature('Product page')
    @allure.story('Product details on Product Page')
    @allure.title('Product has all the necessary details')
    @pytest.mark.smoke
    def test_product_details(self, main_page, product_page):
        main_page.open_main_page(2)
        product_title, product_price = main_page.open_product_in_new_tab(
            product_index
        )
        product_page.assert_product_title_and_price(
            product_title, product_price
        )
        product_page.assert_breadcrumbs_product_title()
        product_page.assert_product_quantity()

        product_page.assert_quantity_input_field_is_active()
        product_page.assert_plus_and_minus_buttons_work()

        product_page.assert_add_to_cart_button_is_active()
        product_page.assert_terms_and_conditions()

    @allure.feature('Product page')
    @allure.story('Add product to cart from Product page')
    @allure.title('Successfully add product to cart from Product page')
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        'product_idx, quantity, price', products_test_data
    )
    def test_add_product_to_cart_from_product_page_success(
        # fmt: off
        self, main_page, product_page, alert_page, cart_page,
        product_idx, quantity, price
        # fmt: on
    ):
        main_page.open_main_page(2)
        product_title, product_price = main_page.open_product_in_new_tab(
            product_idx
        )
        product_page.add_product_quantity(quantity)

        product_page.click_add_to_cart_button()
        alert_page.wait_for_alert()
        product_page.click_cart_icon_in_header()

        cart_page.assert_product_cart_title_quantity_price(
            product_title, price, quantity
        )

    @allure.feature('Product page')
    @allure.story('Product page search')
    @allure.title(
        'Successfully search products by their titles on Product page'
    )
    @pytest.mark.smoke
    @pytest.mark.parametrize('product_idx', products_indexes)
    @pytest.mark.parametrize('search_word', search_words)
    def test_product_page_search_success(
        # fmt: off
        self, main_page, product_page, product_idx, search_word
        # fmt: on
    ):
        main_page.open_main_page()
        main_page.open_product_in_new_tab(product_idx)
        product_page.enter_search_word(search_word)
        product_page.assert_search_word_in_found_products_titles(search_word)
