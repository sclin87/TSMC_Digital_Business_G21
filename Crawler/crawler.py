#from sqlite3.dbapi2 import _Statement
import json
from urllib import response
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import socket
import time
import threading
import re
import datetime
import sqlite3
import requests

nltk.download('stopwords')
nltk.download('punkt')

DB_path = "data/WordCount.db"
Flask_server = "http://localhost:5000/word_count"
class GoogleCrawler():
    
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    

    # 網路擷取器
    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    # 網頁解析器
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup
    # 解析後，取<p>文字
    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    
    def word_count(self, text):
        counts = dict()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        #words = text.replace(',','').split()
        for word in words:
            if word not in stop_words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        return counts
    def get_wordcount_json(self, whitelist , dict_data, date):
        data_array = []
        for i in whitelist:
            if(i not in dict_data):
                dict_data[i] = 10
            json_data = {
                'Date' : date,
                'Company' : i , 
                'Count' : dict_data[i]
            }
            data_array.append(json_data)
        return data_array
    def jsonarray_toexcel(self,data_array,out_file='result.xlsx'):
        df = pd.DataFrame(data=data_array)
        df.to_excel(out_file , index=False)
        return
    def jsonarray_to_server(self,data_array):
        for json in data_array:
            response = requests.post(Flask_server, json=json)
            print(response.status_code)
def writeToDB(datas):
    conn = sqlite3.connect(DB_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS WordCountTable (
            Date TEXT NOT NULL,
            Company TEXT NOT NULL,
            WordCount INT NOT NULL,
            PRIMARY KEY (Date, Company)
            );''')
    for dict1 in datas:
        l = list(dict1.values())
        cursor = conn.execute("SELECT WordCount FROM WordCountTable where Date = \"" + str(l[0]) + "\" and Company = \"" + str(l[1]) + "\";")
        has_instance = 0
        WordCount = 0
        for row in cursor:
            WordCount += row[0]
            has_instance = 1
        if(not has_instance):
            conn.execute("INSERT INTO WordCountTable VALUES (\"" + str(l[0]) + "\", \"" + str(l[1]) + "\"," + str(l[2]) + ")")
        else:
            WordCount += l[2]
            conn.execute("UPDATE WordCountTable SET WordCount = \"" + str(WordCount) + "\" where Date = \"" + str(l[0]) + "\" and Company = \"" + str(l[1]) + "\";")
    conn.commit()
    conn.close()
    return

def job(conn,addr):
    buf = ""
    print('connected by ' + str(addr), end='')
    while(1):
        data0 = conn.recv(1024)
        indata = data0.decode('ascii')
        if(len(data0) == 0):
            conn.close()
            break
        #Target_URL = 'https://taipeitimes.com/News/biz/archives/2022/01/20/2003771688'
        if indata[-1] != '\n':
            buf += indata
            continue
        
        Date_URL = buf + indata[:-1]
        buf = ""
        Target_Date = Date_URL.split()[0]
        
        if(len(Date_URL.split()) != 2):
            #print("\033[93m Wrong Format, it should be \"{Date} {URL}\" \033[0m")
            conn.send("\033[93m Error: Format should be \"{Date} {URL}\\n\" \033[0m".encode('ascii'))
            conn.close()
            break
        pattern = re.compile("\d{4}-\d{2}-\d{2}")
        if(not pattern.match(Target_Date)):
            #print("\033[93m", Target_Date, " isn't valid date format.\033[0m")
            conn.send("\033[93m Error: Invalid Date format. \033[0m".encode('ascii'))
            conn.close()
            break
        try:
            L = Target_Date.split("-")
            datetime.datetime(year=int(L[0]),month=int(L[1]),day=int(L[2]))
        except:
            #print("\033[93m " + Target_Date, " is out of bound.\033[0m")
            conn.send(("\033[93m " + Target_Date + " is out of bound.\033[0m").encode('ascii'))
            conn.close()
            break

        Target_URL = Date_URL.split()[1]
        
        try:
            response = crawler.get_source(Target_URL)
            soup = crawler.html_parser(response.text)
        except:
            print("URL is invalid.")
            conn.send("\033[93m Error: URL is invalid.\033[0m".encode("ascii"))
            conn.close()
            break
        orignal_text = crawler.html_getText(soup)
        #print(orignal_text[:100])
        result_wordcount = crawler.word_count(orignal_text)
        whitelist = ['ASML' , 'Applied Materials', 'TSMC']
        print(result_wordcount)
        end_result = crawler.get_wordcount_json(whitelist , result_wordcount, Target_Date)
        print(end_result)
        crawler.jsonarray_toexcel(end_result, str(time.time()) + ".xlsx")
        #writeToDB(end_result)
        crawler.jsonarray_to_server(end_result)
        print('Excel is OK : ' + str(time.time()) + ".xlsx")
        conn.send("Success, Excel is OK.".encode("ascii"))
        break
    conn.close()

if __name__ == "__main__":
    query = "TSMC ASML"
    crawler = GoogleCrawler()
    HOST = '0.0.0.0'
    PORT = 7878
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    threads = []
    
    while(1):
        print("\n\nListen at port 7878:")
        conn, addr = s.accept()
        threads.append(threading.Thread(target = job, args = (conn, addr)))
        threads[len(threads)-1].start()

    for thread in threads:        
       thread.join()
    
    print("End crawler server")
