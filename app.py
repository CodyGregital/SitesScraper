from flask import Flask
from flask import jsonify
from SiteScraperFactory import SiteScraperFactory

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    html = '<p><h1>Проект агрегатора статей с новостных сайтов: </h1></p> \
           <p><ul><li><h3>новости с главной страницы сайта www.tut.by - <a href="/news/tut.by">смотреть</a></h3></li> \
                  <li><h3>новости с главной страницы сайта www.ria.ru - <a href="/news/ria.ru">смотреть</a></h3></li> \
                  <li><h3>новости с главной страницы сайта www.rbc.ru - <a href="/news/rbc.ru">смотреть</a></h3></li> \
                  <li><h3>все новости с перечисленных сайтов - <a href="/news">смотреть</a></h3></li></ul></p>'
    return html


@app.route('/news', methods=['GET'])
def get_all_news():
    all_news = []
    tutby_scraper = SiteScraperFactory.create_scraper('tut.by')
    tutby_res = tutby_scraper.get_articles()
    rbcru_scraper = SiteScraperFactory.create_scraper('rbc.ru')
    rbcru_res = rbcru_scraper.get_articles()
    riaru_scraper = SiteScraperFactory.create_scraper('ria.ru')
    riaru_res = riaru_scraper.get_articles()
    all_news = tutby_res + rbcru_res + riaru_res
    return jsonify({'news': all_news})


@app.route('/news/tut.by', methods=['GET'])
def get_tutby_news():
    tutby_scraper = SiteScraperFactory.create_scraper('tut.by')
    tutby_scraper_result = tutby_scraper.get_articles()
    return jsonify({'news': tutby_scraper_result})


@app.route('/news/rbc.ru', methods=['GET'])
def get_rbcru_news():
    rbcru_scraper = SiteScraperFactory.create_scraper('rbc.ru')
    rbcru_scraper_result = rbcru_scraper.get_articles()
    return jsonify({'news': rbcru_scraper_result})


@app.route('/news/ria.ru', methods=['GET'])
def get_riaru_news():
    riaru_scraper = SiteScraperFactory.create_scraper('ria.ru')
    riaru_scraper_result = riaru_scraper.get_articles()
    return jsonify({'news': riaru_scraper_result})


if __name__ == '__main__':
    app.run(debug=True)