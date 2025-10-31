import allure

from pages import BasePage
from pages.helpers import (
    assert_text,
    assert_product_title,
    assert_products_count,
    assert_product_price,
)


class CartPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.url = self.base_url + '/shop/cart'

        self.empty_cart_message_locator = ('css selector', '.alert-info')
        self.empty_cart_message_expected = 'Your cart is empty!'
        self.cart_icon_locator = ('css selector', '.my_cart_quantity')

        self.product_cart_title_locator = (
            'css selector',
            '#cart_products h6',
        )
        self.product_cart_price_locator = (
            'css selector',
            '#cart_products .oe_currency_value',
        )
        self.remove_cart_button_locator = (
            'css selector',
            'a.js_delete_product',
        )

    @property
    def cart_icon(self):
        self.wait.until(
            self.ec.presence_of_element_located(self.cart_icon_locator)
        )
        return self.find_element(self.cart_icon_locator)

    @property
    def empty_cart_message(self):
        self.wait.until(
            self.ec.visibility_of_element_located(
                self.empty_cart_message_locator
            )
        )
        empty_cart_message_element = self.find_element(
            self.empty_cart_message_locator
        )
        empty_cart_msg = empty_cart_message_element.text.strip()
        return empty_cart_msg

    @property
    def product_cart_price(self):
        self.wait.until(
            self.ec.visibility_of_element_located(
                self.product_cart_price_locator
            )
        )
        product_cart_price_element = self.find_element(
            self.product_cart_price_locator
        )
        product_cart_price = product_cart_price_element.text.strip()
        return product_cart_price

    @property
    def product_cart_title(self):
        self.wait.until(
            self.ec.visibility_of_element_located(
                self.product_cart_title_locator
            )
        )
        product_cart_title_element = self.find_element(
            self.product_cart_title_locator
        )
        product_cart_title = product_cart_title_element.text.strip()
        return product_cart_title

    @property
    def remove_cart_button(self):
        self.wait.until(
            self.ec.element_to_be_clickable(self.remove_cart_button_locator)
        )
        return self.find_element(self.remove_cart_button_locator)

    @allure.step('Assert cart icon has no items')
    def assert_cart_icon_has_no_items(self):
        assert 'd-none' in self.cart_icon.get_attribute(
            'class'
        ), f"Empty cart icon should have attribute d-none, but doesnt't have"
        assert (
            self.cart_icon.text == ''
        ), f'Empty cart icon should have no texts'

    @allure.step('Assert empty cart message')
    def assert_empty_cart_message(self):
        assert_text(self.empty_cart_message, self.empty_cart_message_expected)

    @allure.step('Assert product title, quantity and price')
    def assert_product_cart_title_quantity_price(
        self, expected_title, expected_price, expected_quantity=1
    ):
        actual_title = self.product_cart_title
        assert_product_title(actual_title, expected_title)

        actual_quantity = int(self.product_quantity)
        assert_products_count(actual_quantity, expected_quantity)

        cart_price_clean = self.product_cart_price.replace(',', '')
        actual_price = float(cart_price_clean)

        if isinstance(expected_price, str):
            expected_price_clean = expected_price.replace(',', '')
            expected_price_float = float(expected_price_clean)
        else:
            expected_price_float = float(expected_price)

        assert_product_price(actual_price, expected_price_float)

    @allure.step('Click Remove button in cart so to delete product')
    def remove_product_from_cart(self):
        self.remove_cart_button.click()

    @allure.step('Open Cart page')
    def open_cart_page(self):
        return self.open_page(self.url)
