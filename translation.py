from PIL import Image
import pytesseract
import googletrans

def image_translate(filename):
    translator = googletrans.Translator()
    image = Image.open(filename)

    result_text = pytesseract.image_to_string(image, lang='eng')

    with open('sample.txt', 'w') as f:
        f.write(result_text)

    after_translate_text = translator.translate(result_text, src='en', dest='ko')
    return after_translate_text.text