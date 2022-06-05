from flask import jsonify
from bs4 import BeautifulSoup
import requests
import urllib
import json
import re
from urllib.parse import quote 

secret_path = './secret.json'
with open(secret_path, 'r') as file:
    naver_secret = json.load(file)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# 바코드 번호 입력받아서 crawling
def crawl_with_barcode(barcode):
    try:
        response = requests.get('http://www.koreannet.or.kr/home/hpisSrchGtin.gs1?gtin=' + barcode)
    
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            product_name = soup.select_one('body > div > div.subCont > div > div.contRight.f_left > div:nth-child(4) > dl > div > div.productTit').get_text()
            product_name = product_name.strip()
            product_name = ' '.join(product_name.split()).strip(barcode).strip()

            product_image = soup.select_one('body > div > div.subCont > div > div.contRight.f_left > div:nth-child(4) > dl > div > div.detailImg > div > img').get('src')
    except ValueError:
        raise '해당 바코드 번호에 대한 정보가 없습니다.'

    return jsonify({
        'product_name': product_name,
        'product_image': product_image
    })


# 입력받은 상품명으로 네이버쇼핑 크롤링
def crawl_with_name(name, page):
    result = []
    try:
        url = 'https://openapi.naver.com/v1/search/shop?query={}&display={}'.format(quote(name), page)
        request = urllib.request.Request(url)
        request.add_header('X-Naver-Client-Id', naver_secret['NAVER_API_CLIENT_ID'])
        request.add_header('X-Naver-Client-Secret', naver_secret['NAVER_API_CLIENT_SECRET'])

        response = urllib.request.urlopen(request)
        search_result = json.loads(response.read().decode('utf-8'))['items']
        
        for product in search_result:
            title = cleanhtml(product['title'])   # 상품 이름
            image = product['image']   # 상품 이미지
            lprice = product['lprice']   # 상품 가격 (최저가)
            mallName = product['mallName']   # 상품 판매처
            link = product['link']   # 상품에 대한 링크 (최저가 판매 사이트 링크로 들어갈 수 있음)

            product_json = {
                'title': title,
                'image': image,
                'lprice': lprice,
                'mallName': mallName,
                'link': link
            }
            result.append(product_json)
    except ValueError:
        raise '해당 상품명에 대한 검색 결과가 없습니다.'
    
    return jsonify({
        'search_result': result
    })