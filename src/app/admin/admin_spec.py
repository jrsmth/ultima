import base64
import pytest
from flask import current_app
from src.app.app import app


class AdminSpec:
    client = app.test_client()

    def should_not_allow_destroy_all_games_when_invalid_creds(self):
        response = self.client.get('/flood')
        assert response.status_code == 401

    # TODO :: mock out redis and/or add redis to GH Action
    @pytest.mark.skipif('current_app.config["ENV"] == "prod"')
    def should_allow_destroy_all_games_when_valid_creds(self):
        byte_string = "{0}:{1}".format(
            current_app.config["USERNAME"],
            current_app.config["PASSWORD"]
        ).encode()

        creds = base64.b64encode(byte_string).decode("utf-8")
        response = self.client.get('/flood', headers={"Authorization": "Basic " + creds})
        assert response.status_code == 204
