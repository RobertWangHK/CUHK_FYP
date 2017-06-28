import requests
import random
from bs4 import BeautifulSoup

def submit_url(url):
    html = get_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    #title = soup.title.string
    movie_id = soup.find("div", {"class":"slate"}).find_all('a')
    if movie_id is None:
	return "none"
    temp = movie_id[0]
    return temp["data-video"]
    #return movie_id

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    timeout = random.choice(range(80, 180))
    rep = requests.get(url,headers = header,timeout = timeout)
    rep.encoding = 'utf-8'
    return rep.text

if __name__ == "__main__":
    url = "http://www.imdb.com/title/tt3183660/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2495768482&pf_rd_r=1PG1P6Y0CBF3YR3MST2C&pf_rd_s=right-4&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_otw_t0"
    submit_url(url)
