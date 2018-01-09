from flask import Flask, request, send_file
import mcgenerator.image
from mcgenerator import Generator, TupleGenerator

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

generators = {'inspirational': Generator.from_file('data/quotes2.txt'),
              'potter': Generator.from_file('data/potter.txt'),
              'tuple': TupleGenerator.from_file('data/quotes2.txt'),
              'trumptuples': TupleGenerator.from_file('data/trump_tweets.txt'),
              'trump': Generator.from_file('data/trump_tweets.txt')}

@app.route('/quote/')
def quote():
    length = request.args.get('length', default=30, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)
    # generate the quote
    sentence = generators[generator].generate_sentence(length=length)
    return sentence


@app.route('/meme/')
def meme():
    length = request.args.get('length', default=15, type=int)
    generator = request.args.get('generator', default='inspirational', type=str)
    # generate the quote
    sentence = generators[generator].generate_sentence(length=length)
    # generate captioned image
    captioned_image = mcgenerator.image.get_captioned_image(sentence)
    return send_file(captioned_image, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
