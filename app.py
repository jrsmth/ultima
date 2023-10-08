import sys
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/game-id")
def game():
    return "Welcome, ${player}!"

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["gameId"])

        if isValidGameId(request.form["gameId"]):
            return redirect(url_for("game"))
        else:
            error = "Invalid Credentials. Please try again."

    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run()

def isValidGameId(id):
    if id == "":
        return False
    else:
        return True
