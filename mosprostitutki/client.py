import sys
import argparse
import configparser

from mosprostitutki import MosProstitutki


class Client:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(r'config.ini')  # fix
        self.browser_model = self.config['browser']
        self.elements = self.config['elements']
        self.account_model = self.config['account']

    def __call__(self, method):
        with MosProstitutki(self.elements,
                      executable_path=self.browser_model['executable_path'],
                      proxy=self.browser_model['proxy'],
                      headless=self.browser_model.getboolean('headless')) as browser:
            if browser.login(self.account_model['username'], self.account_model['password']):
                if method == 'del':
                    browser.turn_off_ads()
                elif method == 'pub':
                    for _ in range(2):
                        browser.update_advertisement()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv = [__file__, 'pub']
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    args = parser.parse_args()
    client = Client()
    client(args.method)
