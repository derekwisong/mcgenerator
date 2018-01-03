from flask import Flask, render_template, request, jsonify, send_file
from mcgenerator import Generator
import image
import io

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

generators = {}
generators['inspirational'] = Generator.from_file('quotes2.txt')
generators['potter'] = Generator.from_file('potter.txt')

@app.route('/quote/')
def quote():
    length = request.args.get('length', default=30, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)

    return generators[generator].generate_sentence(length=length)

@app.route('/meme/')
def meme():
    length = request.args.get('length', default=30, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)
    sentence = generators[generator].generate_sentence(length=length)
    im = image.get_image()
    print(im)
    image.draw_caption(im, sentence, top=True)
    img_io = io.BytesIO()
    print(img_io)
    im.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
