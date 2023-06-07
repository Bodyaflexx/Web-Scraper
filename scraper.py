import string
import requests
import os
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.number_of_pages = int(input())
        self.type_of_articles = input()

    def save_articles(self):
        for page_number in range(1, self.number_of_pages + 1):
            direct = f'Page_{page_number}'
            if not os.path.exists(direct):
                os.makedirs(direct)
            url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_number}'
            response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                article_type = article.find("span", {'data-test': 'article.type'}).text.strip()
                if article_type == self.type_of_articles:
                    article_link = article.find("a", {'data-track-action': 'view article'})
                    main_link = 'https://www.nature.com' + article_link.get('href')
                    resp = requests.get(main_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
                    tmp_article = BeautifulSoup(resp.content, "html.parser")
                    article_body = tmp_article.find('p', {"class": "article__teaser"})
                    article_title = article.find('a').get_text()
                    with open(os.path.join(os.getcwd(), direct, self.make_title(article_title)), 'wb') as f:
                        if article_body is not None:
                            f.write(bytes(article_body.text.strip(), "utf-8"))
                        else:
                            pass
        print('Ready')

    @staticmethod
    def make_title(title):
        return title.replace(" ", "_").strip(string.punctuation) + '.txt'


scrap = Scraper()
scrap.save_articles()
