from bs4 import BeautifulSoup
import requests
import csv
import os


class BabyList:

    HEADERS = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Host": "www.babylist.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.base_url = "https://www.babylist.com"
        self.search_url = "{base_url}/store/{search_keyword}"
        self.search_keywords = self.get_search_keywords()

    def get_search_keywords(self):
        return [
            "infant-car-seats",
            "convertible-car-seats"
        ]

    def run(self):

        while len(self.search_keywords) > 0:

            search_keyword = self.search_keywords.pop(0)
            url = self.search_url.format(
                base_url=self.base_url,
                search_keyword=search_keyword
            )
            response = requests.get(
                url,
                headers=self.HEADERS
            )
            soup = BeautifulSoup(response.text, 'html.parser')

            products = soup.select(".row .col-sm-pull-0")
            Scraped_Urls = []
            for item in products:
                prod_url = item.select_one(".Tappable-inactive").get('href')
                product_url = f"{self.base_url}{prod_url}"
                Scraped_Urls.append(product_url)
            self.save_to_csv(Scraped_Urls, search_keyword)

    def save_to_csv(self, Scraped_urls, search_keyword):

        if os.path.exists('Scraped_data.csv'):
            with open('Scraped_data.csv', 'r+', newline='') as f:
                writer = csv.writer(f)
                reader = csv.reader(f)
                data = list(reader)
                data.pop(0)
                for url in Scraped_urls:
                    url_not_exist = True
                    for existing_url, keyword in data:
                        if url == existing_url:
                            url_not_exist = False
                            break

                    if url_not_exist:
                        writer.writerow([url, search_keyword])
        else:
            with open('Scraped_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f"Product Urls", "Search_Keyword"])
                for url in Scraped_urls:
                    writer.writerow([url, search_keyword])


if __name__ == "__main__":
    scraper = BabyList()
    scraper.run()
