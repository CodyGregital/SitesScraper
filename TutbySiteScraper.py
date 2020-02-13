import requests
import time
from bs4 import BeautifulSoup
from SiteScraper import SiteScraper


class TutbySiteScraper(SiteScraper):
    def __init__(self):
        self.name = 'tut.by'
        self.url = 'https://smart.tut.by'

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

        header_link = soup.find('div', id='title_news_block').find_all('a', class_='header_link io-block-link')

        try:
            main_links = soup.find_all('a', class_='entry__link io-block-link')
        except AttributeError as e:
            return None

        # topnews_links = soup.find('div', id='title_news_block').find_all('a', class_='entry__link io-block-link')
        # geo_news_links = soup.find('div', id='geo_news_block').find_all('a', class_='entry__link io-block-link')
        # exclusive_news_links = soup.find('div', id='s_exclusive').find_all('a', class_='entry__link io-block-link')
        # economics_news_links = soup.find('div', id='r9').find_all('a', class_='entry__link io-block-link')
        # press_news_links = soup.find('div', id='r440').find_all('a', class_='entry__link io-block-link')
        # society_news_links = soup.find('div', id='r11').find_all('a', class_='entry__link io-block-link')
        # world_news_links = soup.find('div', id='r3').find_all('a', class_='entry__link io-block-link')
        # culture_news_links = soup.find('div', id='r5').find_all('a', class_='entry__link io-block-link')
        # accidents_links = soup.find('div', id='r103').find_all('a', class_='entry__link io-block-link')
        # finance_news_links = soup.find('div', id='r310').find_all('a', class_='entry__link io-block-link')
        # realty_news_links = soup.find('div', id='r486').find_all('a', class_='entry__link io-block-link')
        # auto_news_links = soup.find('div', id='r7').find_all('a', class_='entry__link io-block-link')
        # sport_news_links = soup.find('div', id='r6').find_all('a', class_='entry__link io-block-link')
        # lady_news_links = soup.find('div', id='r336').find_all('a', class_='entry__link io-block-link')
        # it_news_links = soup.find('div', id='r15').find_all('a', class_='entry__link io-block-link')
        # afisha_news_links = soup.find('div', id='r491').find_all('a', class_='entry__link io-block-link')
        # go_news_links = soup.find('div', id='r607').find_all('a', class_='entry__link io-block-link')
        # partner_news_links = soup.find('div', id='s_partner').find_all('a', class_='entry__link io-block-link')
        # popcorn_news_links = soup.find('div', id='popcorn_block').find_all('a', class_='entry__link io-block-link')

        # tags_with_links = header_link + topnews_links + geo_news_links + exclusive_news_links +\
        #                   economics_news_links + society_news_links + world_news_links +\
        #                   culture_news_links + accidents_links + finance_news_links + realty_news_links +\
        #                   auto_news_links + sport_news_links + lady_news_links + it_news_links + afisha_news_links +\
        #                   partner_news_links + popcorn_news_links + go_news_links  # press_news_links + go_news_links

        tags_with_links = header_link + main_links

        # print('tags with links = ', len(tags_with_links))

        all_links = []
        for i, link in enumerate(tags_with_links):
            all_links.append(link.get('href'))

        links = set(all_links)
        # print('links = ', len(links))
        links = list(links)

        return self.get_article(links)

    def get_article(self, urls):
        articles = []
        for i, link in enumerate(urls):
            article_soup = self.get_html(link)
            # print()

            article_domain_name = 'https://www.tut.by'

            article_link = link
            # print(i + 1, ' Link = ', link)

            article_title = self.get_article_title(article_soup)
            # print('Title = ', article_title)

            article_text = self.get_edit_article_text(self.get_article_text(article_soup))
            # print('Text = ', article_text)

            articles.append({'name': article_domain_name,
                             'link': article_link,
                             'title': article_title,
                             'text': article_text,
                             })
        return articles

    def get_article_title(self, article_s):
        try:
            article_title_e = ' '.join(article_s.find('div', {'class': 'm_header'}).find('h1').text.split())
        except AttributeError as e:
            article_title_e = 'Тоже мне новость!'
            return article_title_e
        return article_title_e

    def get_article_text(self, article_s):
        try:
            article_text_e = article_s.find('div', attrs={'id': 'article_body'})
        except AttributeError as e:
            return None
        return article_text_e

    def get_edit_article_text(self, unedit_text):
        # print(unedit_text)
        # print(type(unedit_text))
        edit_text = []
        if unedit_text is not None:
            list_of_texts = []
            for tag in unedit_text:
                # print(tag.name)
                if tag.name == 'p':
                    list_of_texts.append(' '.join(tag.text.split()))
                elif tag.name == 'h2':
                    list_of_texts.append(' '.join(tag.text.split()))
            edit_text = '\n'.join(list_of_texts)
        else:
            edit_text = 'Эта страница не является новостной статьей!'
        return edit_text


def main():
    pass


if __name__ == '__main__':
    main()
