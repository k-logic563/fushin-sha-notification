import requests
import json
from bs4 import BeautifulSoup

props = [
    {
        'key': 'information',
        'url': 'https://fushinsha-joho.co.jp/search.cgi?pref=広島県',
    },
    {
        'key': 'comment',
        'url': 'https://fushinsha-joho.co.jp/serif.cgi',
    }
]

data = {
    'information': [],
    'comment': []
}

for prop in props :
    # 不審者情報
    res = requests.get(prop['url'])
    soup = BeautifulSoup( res.text, 'html.parser' )

    headlines = soup.find_all('a', class_='headline')

    for link in headlines :
        href = link.get('href')
        title = link.text
        
        if prop['key'] == 'comment' :
            title = title.replace('\t', '').strip()
        
        payload = {
            'href': href,
            'title': title,
        }
        data[prop['key']].append(payload)

with open('data.json', mode = 'wt', encoding = 'utf-8') as file:
    json.dump(data, file, ensure_ascii = False, indent = 2)