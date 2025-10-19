from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages import CartPage, MainPage, AlertPage, DesksPage, ProductPage


def pytest_configure(config):
    project_root = Path(__file__).resolve().parent
    allure_dir = project_root / 'allure-results'
    allure_dir.mkdir(exist_ok=True)
    config.option.allure_report_dir = str(allure_dir)


@pytest.fixture()
def browser(request):
    service = Service(executable_path=ChromeDriverManager().install())

    browser_options = webdriver.ChromeOptions()
    browser_options.page_load_strategy = 'eager'
    browser_options.add_argument('--headless=new')

    browser_options.add_argument('--window-size=1920,1080')
    browser_options.add_argument(
        '--disable-blink-features=AutomationControlled'
    )
    browser_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    )

    browser_options.add_argument('--log-level=3')
    browser_options.add_argument('--disable-logging')
    browser_options.add_argument('--disable-dev-shm-usage')
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--disable-gpu-sandbox')
    browser_options.add_argument('--disable-software-rasterizer')

    browser_options.add_experimental_option(
        'excludeSwitches',
        ['enable-logging', 'enable-automation', 'ignore-certificate-errors'],
    )
    browser_options.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(service=service, options=browser_options)
    print('\nStart browser for test')

    yield browser
    print('\nQuit browser after test')
    browser.quit()


@pytest.fixture()
def main_page(browser):
    return MainPage(browser)


@pytest.fixture()
def desks_page(browser):
    return DesksPage(browser)


@pytest.fixture()
def product_page(browser):
    return ProductPage(browser)


@pytest.fixture()
def alert_page(browser):
    return AlertPage(browser)


@pytest.fixture()
def cart_page(browser):
    return CartPage(browser)


@pytest.fixture()
def cart_with_product(browser, main_page, alert_page, cart_page):
    main_page.open_main_page()
    product_title, product_price = main_page.click_add_to_cart_on_hover_button(
        10
    )
    alert_page.wait_for_alert()

    main_page.click_cart_icon_in_header()
    cart_page.assert_product_cart_title_quantity_price(
        product_title, product_price
    )

    return cart_page
