import allure

from pages import BasePage


class ProductPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.product_title_locator = ('css selector', 'h1')

        self.breadcrumbs_product_title_locator = (
            'css selector',
            '.breadcrumb-item.active span',
        )
        self.minus_button_locator = ('css selector', '.fa.fa-minus')
        self.plus_button_locator = ('css selector', '.fa.fa-plus')
        self.add_to_cart_button_locator = ('css selector', 'a#add_to_cart')

        self.terms_and_conditions_locator = (
            'css selector',
            '.text-muted.mb-0',
        )
        self.terms_and_conditions_title_expected = 'Terms and Conditions'
        self.terms_and_conditions_link_expected = f'{self.base_url}terms'
        self.terms_and_conditions_texts_expected = (
            '30-day money-back guarantee\nShipping: 2-3 Business Days'
        )

    @property
    def add_to_cart_button(self):
        self.wait.until(
            self.ec.presence_of_element_located(
                self.add_to_cart_button_locator
            )
        )
        return self.find_element(self.add_to_cart_button_locator)

    @property
    def breadcrumbs_product_title(self):
        self.wait.until(
            self.ec.visibility_of_element_located(
                self.breadcrumbs_product_title_locator
            )
        )
        breadcrumbs_product_title_element = self.find_element(
            self.breadcrumbs_product_title_locator
        )
        breadcrumbs_product_title = breadcrumbs_product_title_element.text
        return breadcrumbs_product_title

    @property
    def minus_button(self):
        self.wait.until(
            self.ec.presence_of_element_located(self.minus_button_locator)
        )
        return self.find_element(self.minus_button_locator)

    @property
    def plus_button(self):
        self.wait.until(
            self.ec.presence_of_element_located(self.plus_button_locator)
        )
        return self.find_element(self.plus_button_locator)

    @property
    def product_price(self):
        self.wait.until(
            self.ec.visibility_of_element_located(self.products_prices_locator)
        )
        product_price_element = self.find_element(self.products_prices_locator)
        product_price = product_price_element.text.strip()
        return product_price

    @property
    def product_title(self):
        self.wait.until(
            self.ec.visibility_of_element_located(self.product_title_locator)
        )
        product_title_element = self.find_element(self.product_title_locator)
        product_title = product_title_element.text.strip()
        return product_title

    @property
    def terms_and_conditions(self):
        self.wait.until(
            self.ec.presence_of_element_located(
                self.terms_and_conditions_locator
            )
        )
        return self.find_element(self.terms_and_conditions_locator)

    @property
    def terms_and_conditions_link(self):
        return self.terms_and_conditions_link_element.get_attribute('href')

    @property
    def terms_and_conditions_link_element(self):
        return self.terms_and_conditions.find_element('css selector', 'a')

    @property
    def terms_and_conditions_texts(self):
        full_text = self.terms_and_conditions.text.strip()
        title = self.terms_and_conditions_title
        remaining_text = full_text.replace(title, '', 1).strip()
        return remaining_text

    @property
    def terms_and_conditions_title(self):
        terms_and_conditions_title_element = (
            self.terms_and_conditions.find_element('css selector', 'u')
        )
        terms_and_conditions_text = terms_and_conditions_title_element.text
        return terms_and_conditions_text

    @allure.step('Add product quantity on Product page')
    def add_product_quantity(self, quantity):
        current_quantity = int(self.product_quantity)

        while current_quantity < quantity:
            previous_quantity = current_quantity
            self.plus_button.click()
            self.wait_for_quantity_load(previous_quantity)
            current_quantity = int(self.product_quantity)

    @allure.step('Assert Add to cart button is active')
    def assert_add_to_cart_button_is_active(self):
        self.assert_element_is_displayed_and_enabled(self.add_to_cart_button)

    @allure.step(
        'Assert breadcrumbs product title matches original product title'
    )
    def assert_breadcrumbs_product_title(self):
        actual_text = self.breadcrumbs_product_title
        expected_text = self.product_title
        self.assert_text(actual_text, expected_text)

    @allure.step('Assert plus and minus buttons work')
    def assert_plus_and_minus_buttons_work(self):
        self.assert_element_is_displayed_and_enabled(self.plus_button)
        self.assert_element_is_displayed_and_enabled(self.minus_button)

        initial_quantity = int(self.product_quantity)

        self.minus_button.click()
        self.wait_for_quantity_load(initial_quantity, 'decrease')
        self.assert_product_quantity()

        self.plus_button.click()
        self.wait_for_quantity_load(initial_quantity)
        self.assert_product_quantity(expected_quantity=2)

        self.minus_button.click()
        self.wait_for_quantity_load(2, 'decrease')
        self.assert_product_quantity(expected_quantity=initial_quantity)

    @allure.step('Assert product title and price')
    def assert_product_title_and_price(self, expected_title, expected_price):
        actual_title = self.product_title
        self.check_product_title(actual_title, expected_title)

        actual_price = self.product_price
        self.check_product_price(actual_price, expected_price)

    @allure.step('Assert product quantity')
    def assert_product_quantity(self, expected_quantity=1):
        actual_quantity = self.product_quantity
        self.assert_products_count(actual_quantity, expected_quantity)

    @allure.step('Assert quantity input field is active')
    def assert_quantity_input_field_is_active(self):
        self.assert_element_is_displayed_and_enabled(self.quantity_input_field)

    @allure.step('Assert terms_and_conditions')
    def assert_terms_and_conditions(self):
        self.assert_text(
            self.terms_and_conditions_title,
            self.terms_and_conditions_title_expected,
        )
        self.assert_text(
            self.terms_and_conditions_link,
            self.terms_and_conditions_link_expected,
        )
        self.assert_element_is_displayed_and_enabled(
            self.terms_and_conditions_link_element
        )
        self.assert_text(
            self.terms_and_conditions_texts,
            self.terms_and_conditions_texts_expected,
        )

    @allure.step('Click Add to cart button')
    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    def wait_for_quantity_load(
        self, initial_quantity, expected_direction='increase'
    ):
        if expected_direction == 'increase':
            self.wait.until(
                lambda driver: int(self.product_quantity) > initial_quantity
            )
        elif expected_direction == 'decrease':
            if initial_quantity != 1:
                self.wait.until(
                    lambda driver: int(self.product_quantity)
                    < initial_quantity
                )
