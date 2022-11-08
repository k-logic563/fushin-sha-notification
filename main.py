import requests
import re
import time
import folium
import pandas as pd
from bs4 import BeautifulSoup

headline_list = []
url_list = []
address_list = []

convert_number_props = {
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
    pattern = re.compile('|'.join(convert_number_props.keys()))
    address = pattern.sub(lambda x: convert_number_props[x.group()], address)
    return address

# とりあえず広島県で固定する
res = requests.get('https://fushinsha-joho.co.jp/search.cgi?pref=広島県')
soup = BeautifulSoup( res.text, 'html.parser' )
data = soup.find_all('a', class_='headline')

for index, row in enumerate(data) :
    try :
        _headline = row.text.strip()
        _href = row.get('href')
        _address = get_address(_href)
        
        headline_list.append(_headline)
        url_list.append(_href)
        address_list.append(_address)
    except :
        continue
    time.sleep(1)

df = pd.DataFrame(
    data = {'headline': headline_list, 'url': url_list, 'address': address_list}
)

# 広島データを抽出
df_geo = pd.read_csv('japanese-addresses/latest.csv')
df_geo_hiroshima = df_geo[df_geo.都道府県名 == '広島県']
df_geo_hiroshima = df_geo_hiroshima.copy()
df_geo_hiroshima.loc[:, 'address'] = df_geo_hiroshima.市区町村名 + df_geo_hiroshima.大字町丁目名

# 緯度経度
df_merge = df.merge(df_geo_hiroshima, on='address')
pattern = r"(?P<use>^.*）)(?P<nouse>\d+)"
replace = lambda m: m.group('use').swapcase()
df_merge = df_merge.copy()
df_merge.loc[:, 'headline'] = df_merge.headline.str.replace(pattern, replace)
# マップ生成 広島県庁を中心に
map = folium.Map(location=[34.39678032975633, 132.45960985216675], zoom_start = 10)

for i, r in df_merge.iterrows():
    folium.Marker(
        location = [r['緯度'], r['経度']],
        popup = folium.Popup(
            f'<a href=" { r.url } "target="_blank">{ r.headline }</a>',
            max_width = 300, min_width = 100
        )
    ).add_to(map)
    
map.save("index.html")