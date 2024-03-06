from bs4 import BeautifulSoup
import requests
import mysql.connector as mysql


class CarCare:

    def __init__(self):
        self.base_url = "https://autohub.pk/collections/car-care-products?page={page_no}"

    def run(self):

        page_no = 1
        while True:
            url = self.base_url.format(page_no=page_no)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            next_page = soup.select("li.next a")
            # print(next_page)
            if not next_page:
                break

            else:
                page_no += 1
            print(f"Making Request To Url = {url}")

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            scraped_products = []
            products = soup.select("div.product-desc")
            for item in products:
                name = item.select_one("h3.product-title").text
                price = item.select_one("p.product-price").text.strip()
                # print(price)
                if price:
                    price = price.split('Rs.')[1].strip()

                scraped_products.append((name, price))
            # self.save_in_db(scraped_products)
            print(scraped_products)

    def save_in_db(self, values):

        db = mysql.connect(
            host='localhost',
            user='root',
            passwd='ahmed331',
            database='autohub'
        )
        print("DATABASE IS CONNECTED SUCCESSFULLY!")
        cursor = db.cursor()

        data_base = cursor.execute("CREATE DATABASE IF NOT EXISTS autohub")
        if data_base:
            print("DataBase is created successfully!")

        table = cursor.execute("""
        CREATE TABLE IF NOT EXISTS scrapy ( Product_Name VARCHAR(255) PRIMARY KEY,
        Product_Price VARCHAR(255))
         """)
        if table:
            print("TABLE created successfully!")
        print("INSERTING DATA....")
        query = "INSERT IGNORE INTO scrapy (Product_Name, Product_Price) VALUES (%s, %s)"

        execution = cursor.executemany(query, values)
        db.commit()
        print(cursor.rowcount, ' record inserted')
        if not execution:
            print("PLEASE CHECK RECORDS EXISTS ALREADY!")


if __name__ == "__main__":
    scraper = CarCare()
    scraper.run()


