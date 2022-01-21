from __future__ import annotations

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Browser:
    def __init__(self, executable_path='chromedriver', headless=False, proxy=None) -> None:
        opts = ChromeOptions()
        opts.headless = headless
        if proxy:
            opts.add_argument('--proxy-server=%s' % proxy)
        service = Service(executable_path=executable_path)
        self.driver = Chrome(options=opts, service=service)

    def __enter__(self) -> Browser:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.quit()

    def wait_element(self, xpath, timeout=5) -> WebElement | None:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                lambda d: self.driver.find_element(By.XPATH, xpath),
                'Unable to locate %s ' % xpath
            )
            return element
        except TimeoutException as error:
            logging.error('%s was caught in Browser.wait_element' % error)
            return None

    def wait_element_disappeared(self, xpath, timeout=5) -> bool:
        try:
            element = WebDriverWait(self.driver, timeout).until_not(
                lambda d: self.driver.find_element(By.XPATH, xpath),
                'Unable to locate %s ' % xpath
            )
            return True
        except TimeoutException as error:
            logging.error('%s was caught in Browser.wait_element_disappeared' % error)
            return False
