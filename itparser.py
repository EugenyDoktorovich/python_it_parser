from wsgiref import headers
import requests
from bs4 import BeautifulSoup as bs
import time

import sqlite3
from sqlite3 import Error

#Parsing with requests & bf4
def newsParser():
    url = 'https://ria.ru/technology/'
    news_dict = {}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    result = requests.get(url,headers = headers)

    soup = bs(result.text,'html.parser')

    news_name = soup.find_all('a',class_='list-item__title')

    for title in news_name:
        news_dict[title.string] = title['href']
    
    return news_dict

#Initialization and work with the database sqlite3

def sql_connection():
 
    try:
 
        con = sqlite3.connect('riaitnews.db')
 
        return con
 
    except Error:
 
        print(Error)
 
def sql_table(con): 
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE news4( описание text, ссылка text)")
    print('Таблица успешно создана.')
    con.commit()
 

def dbsaver():
    con = sql_connection()
    print('Подключение к БД успешно.')
    cursor = con.cursor()
    print('Курсор создан успешно.')

    news_dict = newsParser()
    for news in news_dict:
        cursor.execute("INSERT INTO news4 VALUES('{0}','{1}')".format(news,news_dict[news])) 
    print('Данные добавлены в БД.')

    sqlite_select_query = """SELECT * from news4"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    for row in records:
        print("Описание:", row[0])
        print("Ссылка:", row[1])


#Here I call a function in an infinite loop, and set a delay of 24 hours using the time module
while True:
    dbsaver()
    print('''Данные успешно спарсились и добавлены в базу данных, следуюущее обновление через сутки.
    Чтобы прервать работу программы надо нажать ctr+c, по крайней мере в VScode''')
    time.sleep(86400)
    


