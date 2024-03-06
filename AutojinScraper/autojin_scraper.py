from bs4 import BeautifulSoup
import requests
import mysql.connector as mysql


class CarInterior:

    def __init__(self):
        self.base_url = "https://autojin.pk/interior-accessories?page={page_no}"

    def datascrape(self):
        page_no = 1
        while True:
            url = self.base_url.format(page_no=page_no)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            last_one = soup.select("#products .h5")
            if last_one:
                break

            print(
                f"Making Request To Page Number = {page_no} "
                f"URL IS: {url}"
            )
            page_no += 1

            products = soup.select("div.product-info")
            scraped_products = []
            for item in products:
                name = item.select_one(".product-title").text
                price = item.select_one("span.price").text

                values = (name, price)
                scraped_products.append(values)
            self.save_in_db(scraped_products)
            print(scraped_products)

    def save_in_db(self, values):

        db = mysql.connect(
            host='localhost',
            user='root',
            passwd='ahmed331',
            database='autojin',
            port=3306
        )
        if db:
            print("CONNECTED SUCCESSFULLY!")
        cursor = db.cursor()

        data_base = cursor.execute("CREATE DATABASE IF NOT EXISTS autojin")
        if data_base:
            print("DATABASE IS CREATED SUCCESSFULLY!")

        table = cursor.execute("""
            CREATE TABLE IF NOT EXISTS scrapy (id INT(11) AUTO_INCREMENT PRIMARY KEY,
             Product_Name VARCHAR(255),Product_Price VARCHAR(255))
             """)
        if table:
            print("TABLE created successfully!")

        print("INSERTING DATA..")
        query = "INSERT INTO scrapy (Product_Name, Product_Price) VALUES (%s, %s)"

        cursor.executemany(query, values)

        db.commit()

        print(cursor.rowcount, ' record inserted')


if __name__ == "__main__":
    scraper = CarInterior()
    scraper.datascrape()




