# Web Scraper for Emergency Medical Products: Vial Medications

## Instructions
First download the requirements listed below.
Once downloaded, run the command 
#### 'Python Scraper.py path/to/your/database.db'
If you do not input a path, the script will prompt you to input one before proceeding

#### Output: In csv format: all products ordered by price, name descending

## Requirements

### 1. Python
Python is a high level programming language that specializes in simplicity and readability. This script is written
in Python, so you must have it downloaded on your machine to run it

#### Installation
If you do not already have python, visit python.org and follow the installation instructions specific to your machine.

### 2. SQLite
SQLite is a library that implements a small, fast, self-contained, and highly reliable SQL database engine. It is used 
in this project to store and manage the scraped data.

#### Installation
SQLite comes pre-installed with most versions of Python. If it is not pre-installed, you can download it 
here: https://www.sqlite.org/download.html 


### 3. Requests
Requests is a Python library for making HTTP requests. It abstracts the complexities of making requests, allowing 
programmers to send HTTP requests using Python. In this project, it is used to fetch the web pages to be scraped.

#### Installation
Run 'pip install requests' from your terminal.

### 4. Beautiful Soup
Beautiful Soup is used for pulling data out of HTML files. It abstracts the parsing of the HTML data, allowing
programmers to easily navigate, search, and extract the data they are looking for. Here it is used for exactly that.



#### Installation
Run 'pip install beautifulsoup4' from your terminal.

## How the Scraper Operates
The scraper begins by connecting to a database with the path specified by the user. There are 6 pages of products in the
Vial Medications category on EMP's website. The scraper begins with a for loop, one loop for each page of products on 
the site. Within the for loop, a url is built with a function that was made for returning the current page's url based 
on the url pattern. An HTTP request is then sent to the url. Once the HTTP is returned, Beautiful Soup is used to parse
it. Each product has its own div class called 'product-card'. Using Beautiful Soup, all product cards on the page are 
fetched. The script then loops through each product card, storing the information in a dictionary with 
fields: id (primary key), name, price, out of stock indicator, and the url. 
The id field is made to give each product a unique value to be used as a primary key in the database. 
Data formatting is then done to ensure that price is a float. There is also a check on the status of the price: in stock, 
out of stock, or discontinued. If the product is discontinued, it is not included in the collected data. Otherwise, True 
if in stock or False if out of stock. Each dictionary value is then appended to a list of the products. Once all pages 
are scraped, a SQLite database is set up matching the fields of the product dictionaries. It then batch loads all
(non-discontinued) products into the database. A select query is then performed using SQLite to order the products
by price, name in descending order. Finally the information is printed to the console in csv format

