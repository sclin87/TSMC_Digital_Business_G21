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

nltk.download('stopwords')
nltk.download('punkt')

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
    def get_wordcount_json(self,whitelist , dict_data):
        data_array = []
        for i in whitelist:
            if(i not in dict_data):
                dict_data[i] = 0
            json_data = {
                'Date' : 'Week1',
                'Company' : i , 
                'Count' : dict_data[i]
            }
            data_array.append(json_data)
        return data_array
    def jsonarray_toexcel(self,data_array,out_file='result.xlsx'):
        df = pd.DataFrame(data=data_array)
        df.to_excel(out_file , index=False)
        return

def job(conn,addr):
    url = ""
    print('connected by ' + str(addr))
    while(1):
        data0 = conn.recv(1024)
        indata = data0.decode('ascii')
        if(len(data0) == 0):
            conn.close()
            break
        #Target_URL = 'https://taipeitimes.com/News/biz/archives/2022/01/20/2003771688'
        if indata[-1] != '\n':
            url += indata
            continue
        
        Target_URL = url + indata[:-1]
        url = ""

        response = crawler.get_source(Target_URL)
        soup = crawler.html_parser(response.text)
        orignal_text = crawler.html_getText(soup)
        print(orignal_text[:100])
        result_wordcount = crawler.word_count(orignal_text)
        result_wordcount
        whitelist = ['ASML' , 'Intel', 'TSMC']
        end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
        print(end_result)
        crawler.jsonarray_toexcel(end_result, str(time.time()) + ".xlsx")
        print('Excel is OK')
        #s.close()

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
        print("Listen at port 7878:")
        conn, addr = s.accept()
        threads.append(threading.Thread(target = job, args = (conn, addr)))
        threads[len(threads)-1].start()

    for thread in threads:        
       thread.join()
    
    print("End crawler server")
