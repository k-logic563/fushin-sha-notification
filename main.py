import json
import boto3
import requests
from bs4 import BeautifulSoup

bucket_name = 'fushinsha-log'
object_key_name = 'data.json'

json_data = {
    'data': [],
}

def lambda_handler(event, context):
    # s3初期化
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(object_key_name)
    # データ取得
    res = requests.get('https://fushinsha-joho.co.jp/search.cgi?pref=広島県')
    soup = BeautifulSoup( res.text, 'html.parser' )
    headlines = soup.find_all('a', class_='headline')
    for link in headlines :
        href = link.get('href')
        title = link.text
        payload = {
            'href': href,
            'title': title,
        }
        json_data['data'].append(payload)
    # s3オブジェクトへ書き込み
    r = obj.put(Body = json.dumps(json_data))

    return {
        'statusCode': 200,
    }
