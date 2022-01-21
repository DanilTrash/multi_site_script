import argparse
import configparser
import logging
import sys

from mosdosug import MosDosug


class Client:
    name = 'Client class'

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.browser_model = self.config['browser']
        self.elements = self.config['elements']
        self.account_model = self.config['account']

    def __call__(self, method) -> None:
        try:
            with MosDosug(self.elements,
                          executable_path=self.browser_model['executable_path'],  # fix
                          headless=self.browser_model.getboolean('headless'),  # fix
                          proxy=self.browser_model['proxy']) as browser:  # fix
                if browser.login(self.account_model['username'], self.account_model['password']):
                    if method == 'del':
                        browser.turn_off_ads()
                    elif method == 'pub':
                        for _ in range(2):
                            browser.update_advertisement()
        except Exception as error:
            logging.info('Error was caught in calling %s' % self.name)
            logging.exception(error)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv = [__file__, 'del']
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    args = parser.parse_args()
    client = Client()
    client(args.method)
