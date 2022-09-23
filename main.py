import requests
from curl_data import(
    urll,
    headers,
    cookies
)
import os
from bs4 import BeautifulSoup
import time
import random
import csv
import json


"""
Скрапинг сайта
https://ecco.ru/men/shoes/all/
"""


def get_data():
    # создал объект ссесии
    sess = requests.Session()    
    
    response = sess.get(url=urll, headers=headers, cookies=cookies)
    
    # создал директорию для сохранения страницы
    if not os.path.exists("data"):
        os.mkdir("data")
    
    # сохранил страницу
    with open("data/ecco_data.html", "w") as file:
        file.write(response.text)
    
    # инфоблок 
    print("[INFO] page recorded")
    
    # читаю страницу в переменную
    with open("data/ecco_data.html") as file:
        src = file.read()
    
    # создал объект BeautifulSoup
    soup = BeautifulSoup(src, "lxml")
    
    # нашел последнюю страницу
    last_page = int(soup.find("div", class_="pages-items").find_all("a", class_="item")[-4].text)
    
    # инфоблок
    print(f"[INFO] total pages: {last_page}")

    # переменная для записи в json
    all_data_json = []

    # переменная для записи в csv
    all_data_csv = []
    
    # генерирую ссылки на каждую страницу
    for page in range(0, last_page + 1):
    # for page in range(0, 1):    #! test
        url = f"https://ecco.ru/men/shoes/all/?p={page}"
        
        response = sess.get(url=url, headers=headers, cookies=cookies)

        # инфоблок
        print(f"[INFO] work with page №: {page + 1}")
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # блок с карточками
        block_cards = soup.find_all('div', class_='product-card')        

        # сбор информации 
        for card in block_cards:
            
            try:                
                card_name = card.find("div", class_='name').text.strip()
            except Exception as ex:
                card_name = "No data"

            try:
                card_price = card.find('div', class_='price').get("data-value")
            except Exception as ex:
                card_price = "No data"

            try:                
                card_link = card.find('noscript').find('a').get('href')
            except Exception as ex:
                card_link = "No data"

            try:
                card_sizes = card.find('div', class_='sizes').find_all('div', class_="size")            

                # раземеры упакую в список
                card_sizes_list = []
            
                for size in card_sizes:
                    card_sizes_list.append(size.text)
            except Exception as ex:
                card_sizes = "No data"            
            
            # print(f"{card_name}\n{card_price}\n{card_sizes_list}\n{card_link}\n")

            # упаковываю данные я записи в json
            all_data_json.append(
                {
                    'card_name': card_name,
                    'card_price': card_price,
                    'card_sizes': card_sizes_list,
                    'card_link': card_link
                }
            )

            # упаковываю данные для записи в csv
            all_data_csv.append(
                [
                    card_name,
                    card_price,
                    card_sizes_list,
                    card_link
                ]
            )

            # рандомная пауза между запросами
            time.sleep(random.randrange(2, 4))

    # инфоблок
    print(f"[INFO] data recording")

    # записываю данные в json
    with open('data/all_data.json', 'w') as file:
        json.dump(all_data_json, file, indent=4, ensure_ascii=False)

    # записываю данные в csv
    with open('data/all_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'card_name',
                'card_price',
                'card_sizes',
                'card_link'
            )
        )
        writer.writerows(all_data_csv)

    # инфоблок
    print(f"[INFO] code completed!")  


def main():
    get_data()
    
    
if __name__ == "__main__":
    main()
