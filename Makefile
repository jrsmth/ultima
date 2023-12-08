make build:
	sass --update src/resources/static/styles/scss:src/resources/static/styles/css

env = "dev"
# local : make sure local redis is running
# dev   : ensure IP is whitelisted on render redis
# prod
make start:
	export FLASK_ENV=$(env) && make build && gunicorn -b 0.0.0.0:8080 -k gevent -w 1 --chdir src/app app:app

make test:
	export FLASK_ENV="dev" && python3 -m pytest src

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis

make docker:
	docker build -t jrsmiffy/ultima . && docker run --name ultima -p 8080:8080 -d jrsmiffy/ultima
