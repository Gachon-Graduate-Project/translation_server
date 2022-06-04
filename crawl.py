from itertools import product
from xml.dom import NotFoundErr
from flask import jsonify
import requests
from bs4 import BeautifulSoup

# 바코드 번호 입력받아서 crawling
def crawl_with_barcode(barcode):
    try:
        response = requests.get('http://www.koreannet.or.kr/home/hpisSrchGtin.gs1?gtin=' + barcode)
    
        if response.status_code == 200:
            result = response.text
            soup = BeautifulSoup(result, 'html.parser')

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
def crawl_with_name(name):
    try:
        response = requests.get('https://search.shopping.naver.com/search/all?query=' + name) 
    except ValueError:
        raise '해당 상품명에 대한 정보가 없습니다.'