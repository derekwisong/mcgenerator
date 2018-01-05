from flask import Flask, request, send_file
import image

from mcgenerator import Generator

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

generators = {'inspirational': Generator.from_file('data/quotes2.txt'),
              'potter': Generator.from_file('data/potter.txt')}


@app.route('/quote/')
def quote():
    length = request.args.get('length', default=30, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)
    # generate the quote
    sentence = generators[generator].generate_sentence(length=length)
    return sentence


@app.route('/meme/')
def meme():
    length = request.args.get('length', default=30, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)
    # generate the quote
    sentence = generators[generator].generate_sentence(length=length)
    # generate captioned image
    captioned_image = image.get_captioned_image(sentence)
    return send_file(captioned_image, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
