import requests
from bs4 import BeautifulSoup
import time
import re
from SiteScraper import SiteScraper


class RiaruSiteScraper(SiteScraper):
    def __init__(self):
        self.name = 'ria.ru'
        self.url = 'https://ria.ru'

    def get_html(self, url):
        headers = {'accept': '*/*',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/79.0.3945.130 Safari/537.36'}
        try:
            time.sleep(0.5)
            r = requests.get(url, headers=headers, allow_redirects=False)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(r.text, 'lxml')

    def get_articles(self):
        soup = self.get_html(self.url)

        try:
            tags_with_links = soup.find_all('span', {'data-url': True})
        except AttributeError as e:
            return None

        all_links = []
        for i, link in enumerate(tags_with_links):
            all_links.append(link.get('data-url'))

        links = set(all_links)
        links = list(links)

        return self.get_article(links)

    def get_article(self, urls):
        articles = []
        for i, link in enumerate(urls):
            article_soup = self.get_html(link)

            article_domain_name = 'https://www.ria.ru'

            article_link = link

            try:
                longread_type = article_soup.find('div', class_='b-longread')
            except AttributeError as e:
                return None

            if longread_type:
                article_title = self.get_longread_article_title(article_soup)
                article_text = self.get_edit_longread_text(longread_type)
            else:
                article_title = self.get_article_title(article_soup)
                article_text = self.get_edit_article_text(self.get_article_text(article_soup))

            articles.append({'name': article_domain_name,
                             'link': article_link,
                             'title': article_title,
                             'text': article_text,
                             })
        return articles

    def get_longread_article_title(self, article_s):
        try:
            article_title_e = article_s.find('div', class_='endless__item')['data-title']
        except AttributeError as e:
            article_title_e = 'Тоже мне новость!'
            return article_title_e
        return article_title_e

    def get_article_title(self, article_s):
        try:
            article_title_e = ' '.join(article_s.find('h1', {'class': 'article__title'}).text.split())
        except AttributeError as e:
            article_title_e = 'Тоже мне новость!'
            return article_title_e
        return article_title_e

    def get_article_text(self, article_s):
        try:
            article_text_e = article_s.find('div', class_=re.compile('article__body')).\
                                       find_all('div', class_='article__text')
        except AttributeError as e:
            return None
        return article_text_e

    def get_edit_article_text(self, unedit_text):
        if unedit_text is not None:
            list_of_texts = []
            for tag in unedit_text:
                list_of_texts.append(' '.join(tag.text.split()))

            edit_text = '\n'.join(list_of_texts)
        else:
            edit_text = 'Эта страница не является новостной статьей!'
        return edit_text

    def get_edit_longread_text(self, unedit_text):
        if unedit_text is not None:
            list_of_texts = []
            for tag in unedit_text:
                if tag.has_attr('data-pos'):
                    list_of_texts.append(tag.text)

            edit_text = '\n'.join(list_of_texts)
        else:
            edit_text = 'Эта страница не является новостной статьей!'
        return edit_text


def main():
    pass


if __name__ == '__main__':
    main()