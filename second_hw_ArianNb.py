import requests
from bs4 import BeautifulSoup
import logging
import pyodbc
import streamlit as st
import pandas as pd
logger = logging.getLogger()
logging.basicConfig(filename = 'logfile.log', level = 0)
def get_url(item_brand: str, item_name: str, item_price: int, year_from: int, year_to: int):
    url = f"https://divar.ir/s/tehran/car/{item_brand}/{item_name}?price=-{item_price}&production-year={year_from}-{year_to}"
    logger.log(msg = "url is entered by client!", level = 20)
    return url
def is_connection_ok(url: str) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        logger.log(msg = "connection is ok!", level = 20)
        return True
    else:
        logger.log(msg = "connection is not ok!!", level = 20)
        return False
def get_html_of_url(url: str):
    response = requests.get(url)
    if is_connection_ok(url):
        html_page = BeautifulSoup(response.text, 'html.parser')
        return html_page
    else:
        return "html page not found!"
cars = get_url("peugeot", "206", 350000000, 1385, 1395)
print(is_connection_ok(cars))
#
# print(get_url(item_brand="peugeot", item_name="206"))
def get_name_and_price(item_brand: str, item_name: str, item_price: int, year_from: int, year_to: int):
    url = get_url(item_brand, item_name, item_price, year_from, year_to)
    html_page = get_html_of_url(url)
    items = html_page.find_all('div', class_='post-list-eb562')
    items_list = []
    for item in items:
        try:
            item_title = item.find("h2",class_="kt-post-card__title")
            item_price = item.find("div", class_="kt-post-card__description")
            items_list.append((item_title.h2.string[:49], item_price.div.string))
            logger.log(msg = "items's title and price added into list!", level = 20)
        except AttributeError as e:
            pass
    return items_list
def insert_items_info_into_db(items_list: list, server_name: str, database_name: str, table_name: str, item_name: str, item_price: str):
    conn = pyodbc.connect('{ODBC Driver 17 for SQL Server};'
    f'SERVER={server_name};'
    f'DATABASE={database_name};'
    'Trusted_Connection=yes;')
    cursor = conn.cursor()
    insert_query = f"""
    INSERT INTO {table_name} ({item_name}, {item_price}) VALUES(?, ?) 
     """
    cursor.executemany(insert_query, items_list)
    conn.commit()
    print("datas are saved in db!")
    cursor.close()
def streamlit_with_information():
    item_brand = st.text_input('Item brand:')
    item_name = st.text_input('Item name:')
    item_price = st.number_input('Item price:')
    city = st.text_input('City:')
    url = f"https://divar.ir/s/{city}/car/{item_brand}/{item_name}?price=-{item_price}&production-year=1385-1395"
    a = is_connection_ok(url)
    print(a)
    b = get_html_of_url(url)
    print(b)
    btn = st.button('click me!')
    if btn:
        c = pd.DataFrame({
            "برند": [item_brand],
            "نام": [item_name],
            "قیمت": [item_price],
            "شهر": [city]
        })
        st.dataframe(c)
        if __name__ == "__main__":
            streamlit_with_information()