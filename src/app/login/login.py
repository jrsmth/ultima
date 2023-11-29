from flask import render_template, Blueprint, request
from src.app.model.game import Game, generate_game_id, generate_board, has_valid_game_id
from src.app.model.mode.playermode import PlayerMode


# Login Logic
def construct_blueprint(messages, socket, redis):
    login_page = Blueprint('login_page', __name__)

    @login_page.route('/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == "POST":
            game_id = request.form["gameId"]
            user_id = request.form["name"]
            game_mode = request.form["gameMode"]
            player_mode = request.form["playerMode"]
            print(f"[login] Creating game for {user_id}, with game mode [{game_mode}] & player mode [{player_mode}]")

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

                print("[login] Setting game object: " + game.to_string())
                redis.set_complex(game_id, game)
                data = {'gameId': game_id, 'userId': user_id}
                return data, 201

            elif has_valid_game_id(request.form["gameId"]):
                print("Testing playMode [" + request.form["playerMode"] + "]")
                if redis.get("playerMode") == "SINGLE":
                    print("Player Mode set to [SINGLE] for game id [" + redis.get("playerMode") + "]")
                    error = messages.load("login.error.single-player-only")

                else:
                    game = redis.get_complex(game_id)
                    game['player_two']['name'] = request.form["name"]
                    print("[login] Setting game object: " + str(game))
                    redis.set_complex(game_id, game)
                    data = {'gameId': game_id, 'userId': user_id}
                    return data, 201

            else:
                error = messages.load("login.error.invalid-game-id")

        return render_template("login.html", error=error)

    # Blueprint return
    return login_page
