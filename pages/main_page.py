import allure

from pages import BasePage


class MainPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.url1 = self.base_url
        self.url2 = self.base_url + 'shop/page/2'

        self.expected_text_in_product_url = None
        self.product_url = None
        self.product_title = None
        self.product_price = None
        self.hover_cart_button_locator = ('css selector', 'a.a-submit')
        self.product_cart_button = None

    @property
    def products(self):
        self.wait.until(
            self.ec.presence_of_all_elements_located(self.products_locator)
        )
        return self.find_elements(self.products_locator)

    @allure.step('Hover over product and click cart button')
    def click_add_to_cart_on_hover_button(self, product_idx):
        product = self.products[product_idx]
        self.browser.execute_script('arguments[0].scrollIntoView();', product)

        self.product_title = self.get_product_title(product)
        self.product_price = self.get_product_price(product)

        self.actions.move_to_element(product).perform()
        self.product_cart_button = self.get_product_cart_button(product_idx)
        self.wait.until(
            self.ec.element_to_be_clickable(self.product_cart_button)
        )
        self.product_cart_button.click()

        return self.product_title, self.product_price

    def get_product_cart_button(self, product_idx):
        return self.products[product_idx].find_element(
            *self.hover_cart_button_locator
        )

    def get_product_title(self, product):
        self.wait.until(
            self.ec.visibility_of_element_located(self.products_titles_locator)
        )
        product_title = product.find_element(*self.products_titles_locator)
        return product_title.text.strip()

    def get_product_price(self, product):
        self.wait.until(
            self.ec.visibility_of_element_located(self.products_prices_locator)
        )
        product_price = product.find_element(*self.products_prices_locator)
        return product_price.text.strip()

    @allure.step('Open Main page')
    def open_main_page(self, idx=None):
        if idx is None:
            return self.open_page(self.url1)
        elif idx == 2:
            return self.open_page(self.url2)
        return None

    @allure.step('Open product from Main page in new tab')
    def open_product_in_new_tab(self, product_idx):
        product = self.products[product_idx]
        self.product_title = self.get_product_title(product)
        self.product_price = self.get_product_price(product)

        self.open_in_new_tab(product)
        self.product_url = self.browser.current_url

        self.expected_text_in_product_url = (
            self.get_expected_text_in_product_url_from_product_title(
                self.product_title
            )
        )
        assert self.expected_text_in_product_url in self.product_url, (
            f'Product url should contain {self.expected_text_in_product_url}, '
            f'but actual url is {self.product_url}'
        )

        return self.product_title, self.product_price
