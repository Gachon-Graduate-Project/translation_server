from flask import jsonify
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.parse import quote 

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
    url = "https://search.shopping.naver.com/search/all?frm=NVSHMDL&origQuery=&pagingIndex={}&pagingSize=10&productSet=model&query={}&sort=price_asc&timestamp=&viewType=list".format(page, quote(name))
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    
    



crawl_with_name('감자칩', 1)