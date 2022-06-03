from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
import requests
import sys, os, time, schedule, socket

service_host = os.getenv("SERVICE_HOST")
service_port = int(os.getenv("SERVICE_PORT"))
#service_host = "140.113.68.204"
#service_port = 7878

class UrlGenerator():
    def __init__(self):
        self.url = 'https://www.google.com/search?q='
        self.results = []

    # Google search with queries and parameters
    def google_search(self, query, time='qdr:m', num='100', retry=10):
        search_url = self.url + query + \
            '&tbm=nws&tbs={time}&num={num}&lr=lang_en'.format(time=time, num=num)
        response = self.get_source(search_url)
        retry_count = 0
        while response is None:
            print('Retrying Connection ...', file=sys.stderr)
            retry_count += 1
            if retry_count > retry:
                print('Reached Retry Limit', file=sys.stderr)
                os._exit(-1)
            response = self.get_source(search_url)

        self.parse_googleResults(response)

    def get_source(self, url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e, file=sys.stderr)
            return None

    # Google Search Result Parsing
    def parse_googleResults(self, response):
        css_identifier_title = "mCBkyc y355M JQe2Ld nDgy9d"
        css_identifier_link = "WlydOe"
        soup = BeautifulSoup(response.text, 'html.parser')

        titles = soup.findAll("div", {"class": css_identifier_title})
        links = soup.findAll("a", {"class": css_identifier_link})
        for title, link in zip(titles, links):
            self.results.append({'title': title.get_text() ,'link': link['href']})


urlGenerator = UrlGenerator()


def time_str():
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d, %H:%M:%S", t)
    return current_time

def generate_url():
    query = "TSMC "
    supplier = ["Applied Materials", "ASML", "SUMCO"]
    results = []
    for sup in supplier:
        urlGenerator.google_search(query+sup, time='qdr:m', num='100')
        # print(sup + ":")
        for res in urlGenerator.results:
            # print('-', res['title'])
            if res['link'] not in results:
                results.append(res['link'])
        urlGenerator.results.clear()
    return results

def send_links(links):
    try:
        print('Sending Links ...')
        for link in links:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((service_host, service_port))
            print('-', link)
            outstr = link + '\n'
            sock.sendall(outstr.encode('ascii'))
            sock.close()
    except socket.error as e:
        print(e, file=sys.stderr)
        os._exit(1)


# Repeat the Job every hour
#@schedule.repeat(schedule.every().hour)
@schedule.repeat(schedule.every(30).seconds)
def job():
    print(time_str())
    results = generate_url()
    send_links(results)
    


if __name__ == '__main__':
    # Initial Job
    job()

    # Check pending job every 5 minutes
    while True:
        schedule.run_pending()
        time.sleep(10)