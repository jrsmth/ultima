import logging
from flask import Blueprint, Response, current_app
from werkzeug.security import generate_password_hash, check_password_hash


# Admin Logic
def construct_blueprint(auth, redis):
    admin_page = Blueprint('admin_page', __name__)
    log = logging.getLogger(__name__)

    username = current_app.config["USERNAME"]
    password = current_app.config["PASSWORD"]

    users = {
        username: generate_password_hash(password),
    }

    @auth.verify_password
    def verify_password(user, pwd):
        if user in users and check_password_hash(users.get(user), pwd):
            return user

    @admin_page.route("/flood")
    @auth.login_required
    def destroy_all_games():
        log.warning(f"[destroy_all_games] Request to wipe data from {auth.current_user()}")
        redis.clear()
        return Response(status=204, response="The flood is over, Noah")

    # Blueprint return
    return admin_page
