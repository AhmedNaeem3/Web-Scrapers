import json
import csv
import os.path

from bs4 import BeautifulSoup
import requests


class BabyListProductScraper:

    def __init__(self):
        self.input_records = self.get_input_records()

    def get_input_records(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        base_dir = os.path.dirname(current_dir)

        csv_file = os.path.join(base_dir, 'KeywordScraper', 'Scraped_data.csv')
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
                data.pop(0)
                return data
        else:
            return "File doesn't exists!"

    def run(self):

        while len(self.input_records) > 0:
            url, search_keyword = self.input_records.pop(0)
            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find('div', attrs={"data-react-class": "Store"}).get("data-react-props")
            json_data = json.loads(products)
            self.parse(json_data, search_keyword)

    def parse(self, json_data, search_keyword):

        product_data = json_data.get("collections", {})
        for keyword in product_data.keys():
            product_data = product_data.get(keyword)[0]
            break
        product = product_data.get("products")

        product_name = product_data.get("name")
        brand = product_data.get("brand")
        ratings = product_data.get("rating")
        reviews = product_data.get("reviewCount")
        product_url = product_data.get("seoUrl")
        Scraped_data = []
        for item in product.values():
            product_id = item.get("id")
            product_color = item.get("attributes", {}).get("color")
            images = [image.get("url") for image in item.get("images", [])]
            price = item.get("price", {}).get("current")
            Scraped_data.append((
                product_name,
                product_color,
                product_id,
                price,
                ratings,
                reviews,
                brand,
                images,
                product_url,
                search_keyword
            ))
        self.save_to_csv(search_keyword, Scraped_data)

    def save_to_csv(self, search_keyword, Scraped_data):

        if os.path.exists(f"{search_keyword}.csv"):
            with open(f"{search_keyword}.csv", 'r+') as file:
                writer = csv.writer(file)
                reader = csv.reader(file)
                data = list(reader)
                data.pop(0)
                for data in Scraped_data:
                    writer.writerow(data)
        else:
            with open(f"{search_keyword}.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Product_name",
                    "Product_color",
                    "Product_id",
                    "Price",
                    "Ratings",
                    "Reviews",
                    "Brand",
                    "Images",
                    "Product_url",
                    "Search_keyword"
                ])
                for data in Scraped_data:
                    writer.writerow(data)


if __name__ == "__main__":
    Scraper = BabyListProductScraper()
    Scraper.run()
