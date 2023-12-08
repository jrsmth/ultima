import pytest
from src.app.app import app, redis
from flask import current_app


class LoginSpec:
    client = app.test_client()

    # TODO :: mock out redis and/or add redis to GH Action
    @pytest.mark.skipif('current_app.config["ENV"] == "prod"')
    def should_load_login_page_without_error(self):
        response = self.client.get("/", content_type="html/text")
        assert response.status_code == 200
        assert "Player Name" in response.data.decode('utf-8')

    # TODO :: mock out redis and/or add redis to GH Action
    @pytest.mark.skipif('current_app.config["ENV"] == "prod"')
    @pytest.mark.parametrize("game_mode,player_mode", [
        ("standard", "single"),
        ("standard", "double"),
        ("ultimate", "single"),
        ("ultimate", "double")
    ])
    def should_create_game_with_game_and_player_modes(self, game_mode, player_mode):
        data = {
            "name": "test",
            "gameId": "",
            "gameMode": game_mode,
            "playerMode": player_mode
        }

        response = self.client.post("/", data=data)
        location = response.headers["Location"]

        game_id = location.split("/")[2]
        game_state = redis.get_complex(game_id)
        assert game_state["game_mode"] == game_mode
        assert game_state["player_mode"] == player_mode

        assert response.status_code == 302
        assert "/game" in location
