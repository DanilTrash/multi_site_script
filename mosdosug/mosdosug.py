from __future__ import annotations

import argparse
import configparser
import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser


class MosDosug(Browser):
    name = 'MosDosug class'
    base_url = 'https://e.mosdosugs.info'

    def __init__(self, elements, **kwargs) -> None:
        self.elements = elements
        Browser.__init__(self, **kwargs)

    def login(self, username=None, password=None) -> bool:
        url = self.base_url + '/login-form'
        try:
            self.driver.get(url)
            self.wait_element(self.elements['login_username']).send_keys(username)
            self.wait_element(self.elements['login_password']).send_keys(password)
            self.wait_element(self.elements['login_submit']).click()
            return True
        except Exception as error:
            logging.info('Error was caught in calling authorisation')
            logging.exception(error)
            return False

    def turn_off_ads(self):
        url = self.base_url + '/account/'
        try:
            if self.driver.current_url != url:
                self.driver.get(url)
            self.wait_element(self.elements['select_all_ads_checkbox']).click()
            time.sleep(1)
            self.wait_element(self.elements['actions_list']).click()
            self.wait_element(self.elements['turn_off_ads_button']).click()
            time.sleep(1)
            self.wait_element(self.elements['attention_button']).click()
            time.sleep(1)
            return True
        except Exception as error:
            logging.info('Error was caught in calling authorisation')
            logging.exception(error)
            return False

    def update_advertisement(self):
        url = self.base_url + '/account/'
        try:
            if self.driver.current_url != url:
                self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                lambda d: self.driver.execute_script('return document.readyState') == 'complete'
            )
            ads = self.driver.find_elements(By.XPATH, self.elements['ads_elements'])
            for ad in ads:
                status = ad.find_element(By.XPATH, self.elements['advertisement_status']).text
                if status == 'Бесплатно':
                    checkbox = ad.find_element(By.XPATH, self.elements['adv_checkbox'])
                    checkbox.click()
                    change_status = ad.find_element(By.XPATH, self.elements['change_status'])
                    change_status.click()
                    return True
        except Exception as error:
            logging.info('Error was caught in calling authorisation')
            logging.exception(error)
            return False
