from __future__ import annotations

import configparser
from time import sleep

from erobodio import EroBodio


class Client:
    name = 'Client class'

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(r'config.ini')  # fix
        self.browser_model = self.config['browser']
        self.elements = self.config['elements']
        self.account_model = self.config['account']

    def __call__(self, *args, **kwargs):
        with EroBodio(self.elements,
                      executable_path=self.browser_model['executable_path'],
                      proxy=self.browser_model['proxy'],
                      headless=self.browser_model.getboolean('headless')) as browser:
            if browser.login(self.account_model['username'], self.account_model['password']):
                browser.update_advertisement()


if __name__ == '__main__':
    while True:
        client = Client()
        client()
        sleep(7*60)
