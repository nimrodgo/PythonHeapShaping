from flask import Flask, request
import games
from compound import Compound

FLAG = 'CTF{This is an example flag}'


def is_allowed(s):
    if FLAG in s:
        raise ValueError('You will not use the flag')
    if 'flag' in s:
        raise ValueError('You will not even reach the flag')
    if 'admin' in s:
        raise ValueError('The admin directory is a no-no')


BASE_CONFIG = {
    'admin': {'flag': FLAG},
    'global_settings': {'volume': 100},
    'games': {
        'baba': games.BabaIsYou,
        'spire': games.SlayTheSpire
    }
}


def run_user_config(user_config):
    config = Compound.load_from_dict(BASE_CONFIG, input_filter=is_allowed)
    config.user = Compound.load_from_dict(user_config)

    for game in config.user.games:
        game_type = getattr(config.games, game.name)
        game_type(game.version, game.settings)


app = Flask(__name__)


@app.route('/run')
def run():
    if not request.json:
        return 'No JSON', 400
    try:
        run_user_config(request.json)
        return 'GG', 200
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run()
