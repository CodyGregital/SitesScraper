import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import time
import json


class SiteScraper(ABC):

    @abstractmethod
    def get_articles(self):
        pass
        # print('abstract method')

    @abstractmethod
    def get_html(self, url):
        pass

    @abstractmethod
    def get_article(self, urls):
        pass

    @abstractmethod
    def get_edit_article_text(self, unedit_text):
        pass


def main():
    pass


if __name__ == '__main__':
    main()