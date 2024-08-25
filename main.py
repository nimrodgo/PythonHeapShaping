from flask import Flask, request
import operations
from compound import Compound
from flag import FLAG


def is_allowed(s):
    if FLAG in s:
        raise ValueError('You will not use the flag')
    if 'flag' in s:
        raise ValueError('You will not even reach the flag')
    if 'admin' in s:
        raise ValueError('The admin directory is a no-no')


DATABASE = {
    'admin': {'flag': FLAG},
    'global_settings': {'volume': 100},
    'operations': {
        'verify': operations.verify
    },
    'public': {
        'version': '1.0.0',
        'author': 'Nimi'
    }
}


def run_query(request):
    config = Compound.load_from_dict(DATABASE, input_filter=is_allowed)
    config.user = Compound.load_from_dict(request, input_filter=is_allowed)

    for query in config.user.queries:
        database_function = getattr(config.operations, query.name)
        database_function(query.data, query.auth)


app = Flask(__name__)


@app.route('/query')
def query():
    run_query(request.json)
    return 'GG', 200


@app.errorhandler(500)
def server_error(e):
    return str(e.original_exception), 500


if __name__ == '__main__':
    app.run()
