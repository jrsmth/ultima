from flask import Flask, render_template

app = Flask(__name__)
# https://github.com/ChristinaVoss/flask-with-sass -> have a look at this

@app.route("/")
def home():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()
