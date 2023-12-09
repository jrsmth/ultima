import logging
from flask import redirect, url_for, render_template, Blueprint, request
from src.app.model.game import Game, generate_game_id, generate_board, has_valid_game_id
from src.app.model.mode.playermode import PlayerMode


# Login Logic
def construct_blueprint(messages, redis):
    login_page = Blueprint('login_page', __name__)
    log = logging.getLogger(__name__)

    @login_page.route('/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == "POST":
            game_id = request.form["gameId"]
            user_id = request.form["name"]
            game_mode = request.form["gameMode"]
            player_mode = request.form["playerMode"]
            log.info(f"[login] Creating game for {user_id}, with game mode [{game_mode}] & player mode [{player_mode}]")

            if game_id == "":
                game_id = generate_game_id()
                game = Game()
                game.game_id = game_id
                game.game_mode = game_mode
                game.player_mode = player_mode
                game.player_one.name = request.form["name"]
                game.player_two.name = ""
                game.board = generate_board(game_mode)

                if player_mode == PlayerMode.SINGLE.value:
                    game.player_two.name = "Computer"

                log.debug("[login] Setting game object: " + game.to_string())
                redis.set_complex(game_id, game)
                return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

            elif has_valid_game_id(request.form["gameId"]):
                game = redis.get_complex(game_id)
                log.debug("Testing playMode [" + request.form["playerMode"] + "]")
                if game["player_mode"] == "SINGLE":
                    log.debug("Player Mode set to [SINGLE] for game id [" + redis.get("playerMode") + "]")
                    error = messages.load("login.error.single-player-only")
                else:
                    game['player_two']['name'] = request.form["name"]
                    log.debug("[login] Setting game object: " + str(game))
                    redis.set_complex(game_id, game)
                    return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

            else:
                error = messages.load("login.error.invalid-game-id")

        return render_template("login.html", error=error, games=get_game_info())

    def get_game_info():
        game_info = []
        for key in redis.get_client().scan_iter():
            game = redis.get_complex(key)
            log.debug("[get_game_info] Found game: " + str(game))
            game_id = game["game_id"]
            owner = ''
            player_two = ''
            try:
                owner = game["player_one"]["name"]
            except KeyError:
                log.debug("[get_game_info] No owner found for game with id: " + str(game_id))
            try:
                player_two = game["player_two"]["name"]
            except KeyError:
                log.debug("[get_game_info] No second player found for game with id: " + str(game_id))
            if player_two == '':
                game_info.append((game_id, owner))

        log.info("[get_game_info] Available games: " + str(game_info))
        return game_info

    # Blueprint return
    return login_page
