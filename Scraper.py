import sqlite3
import requests
from bs4 import BeautifulSoup
import sys

# Set up database path
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = input("Please enter the path to the database: ")

# Connect to database
conn = sqlite3.connect(path)
cur = conn.cursor()


# Function to build url from page number
def build_url(page_number):
    return "https://www.buyemp.com/category/vial-medications/793?q=%3Arelevance&page=" + str(page_number) + "&viewMode=grid&pageSize=24&sort="


# Initialize data list
data = []

primary_key = 0

for page_number in range(0, 6):

    url = build_url(page_number)

    response = requests.get(url)

    # If the request is successful
    if response.status_code == 200:
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        # All products on page
        product_cards = soup.find_all('div', class_='grid-card-wrapper')

        # For each product
        for product in product_cards:

            # Fetch product name
            product_name = product.find('h2', class_='card-name').text.strip()

            # Fetch and format price
            card_container = product.find('div', class_='card-container')
            product_price = card_container['data-price'].strip()
            product_price = (product_price.replace(',', '').replace('$', ''))
            if product_price == '':
                product_price = 0.0
            else:
                product_price = float(product_price)

            # Fetch OOS status
            status = product.find('div', class_='status-title')

            # Filter OOS status
            if 'gray' in status['class'] or 'green' in status['class'] or 'blue' in status['class']:
                stock_status = True
            elif 'yellow' in status['class']:
                stock_status = False
            else:
                stock_status = "Discontinued"

            # Only include if not discontinued
            if stock_status != "Discontinued":
                product_details = {
                    'id': primary_key,
                    'name': product_name,
                    'price': product_price,
                    'in_stock': stock_status,
                    'url': url
                }
                primary_key += 1
                data.append(product_details)
            else:
                continue

#  Create table
cur.execute('''CREATE TABLE IF NOT EXISTS product_info
            (id INTEGER PRIMARY KEY,
             name TEXT,
             price REAL,
             in_stock BOOLEAN,
             url TEXT);''')

conn.commit()

for product in data:
    try:
        cur.execute('''
            INSERT INTO product_info (id, name, price, in_stock, url)
            VALUES (?, ?, ?, ?, ?)''',
                    (product['id'], product['name'], product['price'], product['in_stock'], product['url']))
    except sqlite3.IntegrityError:
        print('problem loading database!')
        # Handle insertion issues
        pass

conn.commit()

# Select products in order by price, name
cur.execute('''
    SELECT id, name, price, in_stock, url 
    FROM product_info 
    ORDER BY price DESC, name DESC
''')

# Print data in csv format
print("id, name, price, in_stock, url")
for row in cur.fetchall():
    print(','.join(map(str, row)))

# Close database connections
cur.close()
conn.close()


