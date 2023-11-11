make build:
	sass --update src/resources/static/styles/scss:src/resources/static/styles/css

env = "dev"
# local : make sure redis is running
# dev   : ensure IP is whitelisted on render redis
# prod
make start:
	export FLASK_ENV=$(env) && make build && gunicorn -b 0.0.0.0:8080 --chdir src/app app:app

make test:
	export FLASK_ENV="prod" && python3 -m unittest discover ./src/app

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis

make docker:
	docker build -t jrsmiffy/ultima . && docker run --name ultima -p 8080:8080 -d jrsmiffy/ultima
