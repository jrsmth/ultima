make build:
	sass --update static/styles/scss:static/styles/css

env = "dev" # local / dev / prod
make start:
	export FLASK_ENV=$(env) && make build && gunicorn -b 0.0.0.0:8080 app:app
	# Make sure redis is running

make test:
	python3 -m unittest test

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis

make docker:
	docker build -t jrsmiffy/ultima . && docker run --name ultima -p 8080:8080 -d jrsmiffy/ultima
