from flask import Flask, jsonify
from flask import Blueprint, request
from werkzeug.utils import secure_filename
import translation

app = Flask(__name__)
# bp = Blueprint('image', __name__, url_prefix='/image')

@app.route('/translation', methods=['GET'])
def save_image():
    f = request.files['file']
    filename = './translation_img/' + secure_filename(f.filename)
    f.save(filename)
    return jsonify({
        'after_translate': translation.image_translate(filename)
    })


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)