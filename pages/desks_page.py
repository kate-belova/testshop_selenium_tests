import time

import allure

from pages import BasePage


class DesksPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.url = self.base_url + '/shop/category/desks-1'

        self.desks_found_counter_locator = (
            'css selector',
            '.products_header .oe_search_found',
        )

        self.price_slider_locator = (
            'css selector',
            'input[type="range"].original',
        )

        self.dropdown_sort_by_locator = ('css selector', '.dropdown_sorty_by')
        self.dropdown_options_locator = (
            'css selector',
            '.dropdown_sorty_by a.dropdown-item',
        )

    @property
    def desks_found(self):
        self.wait.until(
            self.ec.presence_of_all_elements_located(self.products_locator)
        )
        return self.find_elements(self.products_locator)

    @property
    def desks_found_counter(self):
        self.wait.until(
            self.ec.visibility_of_element_located(
                self.desks_found_counter_locator
            )
        )
        desks_found_counter = self.find_element(
            self.desks_found_counter_locator
        ).text
        desks_found_counter = (
            desks_found_counter.lstrip('(').split()[0].strip()
        )
        return int(desks_found_counter)

    @property
    def desks_prices(self):
        self.wait.until(
            self.ec.visibility_of_all_elements_located(
                self.products_prices_locator
            )
        )
        desks_prices_elements = self.find_elements(
            self.products_prices_locator
        )
        desks_prices_lst = [
            float(desk_price.text.replace('$', '').replace(',', '').strip())
            for desk_price in desks_prices_elements
        ]
        return desks_prices_lst

    @property
    def dropdown_options(self):
        self.wait.until(
            self.ec.presence_of_all_elements_located(
                self.dropdown_options_locator
            )
        )
        return self.find_elements(self.dropdown_options_locator)

    @property
    def dropdown_sort_by(self):
        self.wait.until(
            self.ec.presence_of_element_located(self.dropdown_sort_by_locator)
        )
        return self.find_element(self.dropdown_sort_by_locator)

    @property
    def price_slider(self):
        self.wait.until(
            self.ec.visibility_of_element_located(self.price_slider_locator)
        )
        return self.find_element(self.price_slider_locator)

    @allure.step(
        'Assert actual count of desks found equals the one in counter'
    )
    def assert_actual_desks_count_equals_the_one_in_counter(self):
        counter_number = self.desks_found_counter
        actual_count = len(self.desks_found)
        self.assert_search_counter_and_actual_amount_found(
            counter_number, actual_count
        )

    @allure.step('Assert desks count')
    def assert_found_desks_count(self, expected_count):
        actual_count = len(self.desks_found)
        self.assert_products_count(actual_count, expected_count)

    @allure.step('Assert desks are sorted by name ascending')
    def assert_sorted_by_name_asc(self):
        titles = self.products_titles
        sorted_titles = sorted(titles)
        assert titles == sorted_titles, (
            f'Titles are not sorted A-Z. '
            f'Expected: {sorted_titles}, Actual: {titles}'
        )

    @allure.step('Assert desks are sorted by price ascending')
    def assert_sorted_by_price_asc(self):
        prices = self.desks_prices
        sorted_prices = sorted(prices)
        assert prices == sorted_prices, (
            f'Prices are not sorted Low to High. '
            f'Expected: {sorted_prices}, Actual: {prices}'
        )

    @allure.step('Assert desks are sorted by price descending')
    def assert_sorted_by_price_desc(self):
        prices = self.desks_prices
        sorted_prices = sorted(prices, reverse=True)
        assert prices == sorted_prices, (
            f'Prices are not sorted High to Low. '
            f'Expected: {sorted_prices}, Actual: {prices}'
        )

    @allure.step('Set comfortable max price on price slider')
    def change_slider_max_price(self, max_price=None):
        current_price_values = self.price_slider.get_attribute('value').split(
            ','
        )
        current_max = float(current_price_values[1])

        if max_price is not None and max_price != current_max:
            self.move_right_thumb(max_price)

        self.wait_for_desks_reload()

    def move_right_thumb(self, max_price):
        slider_min = float(self.price_slider.get_attribute('min'))
        slider_max = float(self.price_slider.get_attribute('max'))
        width = self.price_slider.size['width']

        position_ratio = (max_price - slider_min) / (slider_max - slider_min)
        target_pixels = width * position_ratio

        self.actions.move_to_element(self.price_slider)
        self.actions.move_by_offset(width / 2, 0)
        self.actions.click_and_hold()
        self.actions.move_by_offset(target_pixels - width, 0)
        self.actions.release()
        self.actions.perform()

    @allure.step('Open Desks page')
    def open_desks_page(self):
        return self.open_page(self.url)

    @allure.step('Click dropdown Sort By and choose sort option')
    def select_sort_option(self, index):
        self.dropdown_sort_by.click()
        chosen_option = self.dropdown_options[index]

        self.wait.until(self.ec.element_to_be_clickable(chosen_option))
        self.wait.until(lambda driver: chosen_option.text.strip() != '')
        option_text = chosen_option.text

        chosen_option.click()
        self.wait_for_desks_reload()

        return option_text

    def wait_for_desks_reload(self, timeout=3):
        start_time = time.time()

        initial_desks = self.desks_found
        initial_count = len(initial_desks)

        while time.time() - start_time < timeout:
            current_desks = self.desks_found
            current_count = len(current_desks)

            if current_count != initial_count:
                return True

        return False
