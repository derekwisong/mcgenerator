from flask import Flask, render_template, request, jsonify
from mcgenerator import Generator

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

generator = Generator()
filename = "quotes2.txt"
with open(filename, 'r') as f:
    for line in f:
        generator.read_sentence(line.strip())

@app.route('/')
def hello_world():
    return render_template('index.html', message=generator.generate_sentence())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
