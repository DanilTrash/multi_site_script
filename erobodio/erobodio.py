from __future__ import annotations

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser


class EroBodio(Browser):
    base_url = 'https://www.erobodio.ru'

    def __init__(self, elements, **kwargs):
        self.elements = elements  # fix
        Browser.__init__(self, **kwargs)  # fix
        self.driver.maximize_window()

    def login(self, username, password) -> bool:
        url = self.base_url + '/login'
        try:
            self.driver.get(url)
            self.wait_element(self.elements['login_username']).send_keys(username)
            self.wait_element(self.elements['login_password']).send_keys(password)
            self.wait_element(self.elements['login_submit']).click()
            self.wait_element_disappeared(self.elements['login_submit'])
            return True
        except Exception as error:
            logging.error('EroBodio login error')
            logging.exception(error)
            return False

    def update_advertisement(self):
        url = self.base_url + '/profile'
        try:
            self.driver.get(url)
            medias = self.driver.find_elements(By.XPATH, self.elements['list_of_advertisements'])
            activated_medias = [media for media in medias if 'Включена' in media.text]
            for _ in range(len(activated_medias)):
                medias = WebDriverWait(self.driver, 5).until(
                    lambda d: self.driver.find_elements(By.XPATH, self.elements['list_of_advertisements']))
                activated_medias = [media for media in medias if 'Включена' in media.text]
                for media in activated_medias:
                    status = WebDriverWait(self.driver, 5).until(
                        lambda d: media.find_element(By.XPATH, self.elements['media_status']))
                    _ = status.location_once_scrolled_into_view
                    if 'Включена' in status.text:
                        change_status_button = media.find_element(By.XPATH, self.elements['change_to_free'])
                        if 'Сейчас свободна' in change_status_button.text:
                            change_status_button.click()
                            time.sleep(0.5)
                            self.wait_element(self.elements['approve_status_change']).click()
                            time.sleep(1)
                            print('ad updated')
                            break
            return True
        except Exception as error:
            logging.error('EroBodio update_advertisement error')
            logging.exception(error)
            return False
