import allure
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.helpers import assert_word_in_title


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.base_url = 'http://testshop.qa-practice.com/'
        self.current_url = self.browser.current_url
        self.tabs = None

        self.wait = WebDriverWait(self.browser, 20)
        self.ec = ec
        self.actions = ActionChains(self.browser)

        self.logo_with_link_locator = ('css selector', 'a[href="/"]')
        self.cart_icon_in_header_locator = (
            'css selector',
            'a[href="/shop/cart"]',
        )

        self.products_locator = ('css selector', '.oe_product')
        self.products_titles_locator = (
            'css selector',
            'a[itemprop="name"]',
        )
        self.products_prices_locator = ('css selector', '.oe_currency_value')
        self.quantity_input_field_locator = ('css selector', 'input.quantity')
        self.search_field_locator = (
            'css selector',
            '.o_wsale_products_searchbar_form input',
        )

    @property
    def cart_icon_in_header(self):
        self.wait.until(
            self.ec.element_to_be_clickable(self.cart_icon_in_header_locator)
        )
        return self.find_element(self.cart_icon_in_header_locator)

    @property
    def logo(self):
        self.wait.until(
            self.ec.element_to_be_clickable(self.logo_with_link_locator)
        )
        return self.find_element(self.logo_with_link_locator)

    @property
    def product_quantity(self):
        return self.quantity_input_field.get_attribute('value').strip()

    @property
    def products_titles(self):
        self.wait.until(
            self.ec.visibility_of_all_elements_located(
                self.products_titles_locator
            )
        )
        products_titles_elements = self.find_elements(
            self.products_titles_locator
        )
        products_titles_lst = [
            desk_name.text.strip() for desk_name in products_titles_elements
        ]
        return products_titles_lst

    @property
    def quantity_input_field(self):
        self.wait.until(
            self.ec.presence_of_element_located(
                self.quantity_input_field_locator
            )
        )
        return self.find_element(self.quantity_input_field_locator)

    @property
    def search_field(self):
        self.wait.until(
            self.ec.element_to_be_clickable(self.search_field_locator)
        )
        return self.find_element(self.search_field_locator)

    @allure.step('Click the website logo and go to the Main page')
    def assert_navigation_to_main_page(self):
        self.logo.click()
        self.wait_for_url_to_change(self.current_url)
        assert self.browser.current_url == self.base_url

    @allure.step('Assert search word in found products titles')
    def assert_search_word_in_found_products_titles(self, search_word):
        for title in self.products_titles:
            assert_word_in_title(search_word, title)

    @allure.step('Click cart icon in header')
    def click_cart_icon_in_header(self):
        self.cart_icon_in_header.click()
        self.wait_for_url_to_change(self.current_url)

    @allure.step('Enter key word into search field')
    def enter_search_word(self, search_word):
        self.search_field.clear()
        self.search_field.send_keys(search_word)
        self.search_field.send_keys(Keys.ENTER)

    def find_element(self, args):
        return self.browser.find_element(*args)

    def find_elements(self, args):
        return self.browser.find_elements(*args)

    def open_in_new_tab(self, element):
        self.actions.key_down(Keys.CONTROL).click(element).key_up(
            Keys.CONTROL
        ).perform()

        self.update_tabs()
        new_tab = self.tabs[-1]
        self.browser.switch_to.window(new_tab)

    def open_page(self, url):
        return self.browser.get(url)

    def update_tabs(self):
        self.tabs = self.browser.window_handles

    def wait_for_url_to_change(self, original_url):
        self.wait.until(lambda browser: browser.current_url != original_url)
