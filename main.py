from flask import Flask, request, render_template
from base64 import b64encode
import operations
from compound import Compound
from flag import FLAG
from functools import partial
from functools import wraps


def is_allowed(s):
    if isinstance(s, str):
        s = s.encode()
    if FLAG.encode() in s:
        raise ValueError('You will not use the flag')
    if b'flag' in s:
        raise ValueError('You will not even reach the flag')
    if b'admin' in s:
        raise ValueError('The admin directory is a no-no')

USER_DATA = {
    'videos': {},
    'text': {},
    'images': {}
}

def upload_wrapper(upload_func):
    @wraps(upload_func)
    def func(name, data):
        is_allowed(data)
        return upload_func(USER_DATA, name, data)

    return func

def read_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()


DATABASE = {
    'admin': {'flag': FLAG},
    'global_settings': {'volume': 100},
    'operations': {
        'video': upload_wrapper(operations.upload_video),
        'text': upload_wrapper(operations.upload_text),
        'image': upload_wrapper(operations.upload_image),
    },
    'public': {
        'cat': b64encode(read_file('static/cat.jpg')),
        'space': b64encode(read_file('static/space.mp4')),
        'bee': read_file('static/bee.txt').decode(),
    }
}


def run_query(request):
    config = Compound.load_from_dict(DATABASE, input_filter=is_allowed)
    config.user = Compound.load_from_dict(request, input_filter=is_allowed)

    for query in config.user.queries:
        database_function = getattr(config.operations, query.name)
        database_function(query.file_name, query.data)


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    run_query(request.json)
    return 'Request completed successfully', 200


@app.route('/video/<name>')
def video(name):
    return render_template('video.html', data=b64encode(USER_DATA['videos'][name]).decode())

@app.route('/text/<name>')
def text(name):
    return render_template('text.html', data=USER_DATA['text'][name])

@app.route('/image/<name>')
def image(name):
    return render_template('image.html', data=b64encode(USER_DATA['images'][name]).decode())

@app.errorhandler(500)
def server_error(e):
    return str(e.original_exception), 500


if __name__ == '__main__':
    app.run()
