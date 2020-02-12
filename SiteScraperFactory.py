from RbcruSiteScraper import RbcruSiteScraper
from RiaruSiteScraper import RiaruSiteScraper
from TutbySiteScraper import TutbySiteScraper


class SiteScraperFactory:

    @staticmethod
    def create_scraper(scraper_type):
        try:
            if scraper_type == 'tut.by':
                return TutbySiteScraper()
            if scraper_type == 'rbc.ru':
                return RbcruSiteScraper()
            if scraper_type == 'ria.ru':
                return RiaruSiteScraper()
            raise AssertionError('Scraper not found')
        except AssertionError as _e:
            print(_e)


def main():
    pass


if __name__ == '__main__':
    main()