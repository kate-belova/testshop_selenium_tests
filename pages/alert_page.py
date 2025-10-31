import allure

from pages import BasePage


class AlertPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

        self.alert_locator = ('css selector', '[role="alert"]')

    @property
    def alert(self):
        return self.find_element(self.alert_locator).click()

    @allure.step('Wait for alert to appear')
    def wait_for_alert(self):
        self.wait.until(
            self.ec.presence_of_element_located(self.alert_locator)
        )
