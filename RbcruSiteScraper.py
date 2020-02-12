import requests
from bs4 import BeautifulSoup
import time
import re
from SiteScraper import SiteScraper


class RbcruSiteScraper(SiteScraper):
    def __init__(self):
        self.name = 'rbc.ru'
        self.url = 'https://www.rbc.ru'

    def get_html(self, url):
        headers = {'accept': '*/*',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/79.0.3945.130 Safari/537.36'}
        try:
            time.sleep(0.5)
            r = requests.get(url, headers=headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(r.text, 'lxml')

    def get_articles(self):
        soup = self.get_html(self.url)

        main_news = soup.find_all('a', href=re.compile('from=from_main'))
        center_news = soup.find_all('a', href=re.compile('from=center'))

        tags_with_links = main_news + center_news

        links = []
        for i, link in enumerate(tags_with_links):
            links.append(link.get('href'))

        return self.get_article(links)

    def get_article(self, urls):
        articles = []
        for i, link in enumerate(urls):
            article_soup = self.get_html(link)

            article_domain_name = 'https://www.rbc.ru'

            article_link = link

            article_title = [string for string in
                             article_soup.find('div', class_='article__header__title').stripped_strings][0]

            article_text = self.get_edit_article_text(article_soup.find('div', class_='article__text'))

            articles.append({'name': article_domain_name,
                             'link': article_link,
                             'title': article_title,
                             'text': article_text,
                             })
        return articles

    def get_edit_article_text(self, unedit_text):
        try:
            list_of_texts = []
            list_of_texts.append([string for string in
                                 unedit_text.find('div', class_='article__text__overview').stripped_strings][0])

            for tag in unedit_text:
                if tag.name == 'p':
                    list_of_texts.append(' '.join(tag.text.split()))

            edit_text = '\n'.join(list_of_texts)
        except AttributeError:
            return None
        return edit_text


def main():
    pass


if __name__ == '__main__':
    main()