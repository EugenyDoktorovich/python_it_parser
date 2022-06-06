from wsgiref import headers
import requests
from bs4 import BeautifulSoup as bs

import sqlite3
from sqlite3 import Error

#Сбор инфы
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

#БД

def sql_connection():
 
    try:
 
        con = sqlite3.connect('riaitnews.db')
 
        return con
 
    except Error:
 
        print(Error)
 
def sql_table(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE news4( описание text, ссылка text)")
 
    con.commit()
 
con = sql_connection()
cursor = con.cursor()

news_dict = newsParser()
for news in news_dict:
    cursor.execute("INSERT INTO news4 VALUES('{0}','{1}')".format(news,news_dict[news])) 


sqlite_select_query = """SELECT * from news4"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
for row in records:
    print("Описание:", row[0])
    print("Ссылка:", row[1])
