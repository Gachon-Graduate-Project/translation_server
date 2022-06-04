from flask import Flask, jsonify
from flask import Blueprint, request
from werkzeug.utils import secure_filename
import translation, crawl

app = Flask(__name__)
# bp = Blueprint('image', __name__, url_prefix='/image')

@app.route('/translation', methods=['GET'])
def save_translation_image():
    f = request.files['file']
    filename = './translation_img/' + secure_filename(f.filename)
    f.save(filename)
    return jsonify({
        'after_translate': translation.image_translate(filename)
    })


@app.route('/barcode/<barcode_number>', methods=['GET'])
def crawl_with_brcode(barcode_number):
    # 바코드 번호 받아와서 해당 번호로 크롤링 진행
    return crawl.crawl_with_barcode(barcode_number)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)