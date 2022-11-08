import requests
import re
from bs4 import BeautifulSoup

headlines = []
url_list = []
address_list = []

d = {
    '１':'一',
    '２':'二',
    '３':'三',
    '４':'四',
    '５':'五',
    '６':'六',
    '７':'七',
    '８':'八',
    '９':'九',
}
def get_address(url):
    # 住所抽出
    pattern = re.compile('^.*）(.*?)(付近)*で.*')
    html = requests.get(url).content.decode('utf-8')
    soup2 = BeautifulSoup(html, 'html.parser')
    address = pattern.match(soup2.title.text).group(1)
    #漢数字変換
    pattern = re.compile('|'.join(d.keys()))
    address = pattern.sub(lambda x: d[x.group()], address)
    return address

# とりあえず広島県で固定する
res = requests.get('https://fushinsha-joho.co.jp/search.cgi?pref=広島県')
soup = BeautifulSoup( res.text, 'html.parser' )
data = soup.find_all('a', class_='headline')

for i, row in enumerate(data) :
    try :
        headline = row.text.strip()
        href = row.get('href')
        # address = get_address(href)
        
        headlines.append(headline)
        url_list.append(href)
        # address_list.append(address)
    except :
        continue
    
print(headlines)
