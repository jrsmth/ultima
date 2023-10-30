make build:
	sass --update app/resources/static/styles/scss:app/resources/static/styles/css

env = "local" # local / dev / prod
make start:
	export FLASK_ENV=$(env) && make build && gunicorn -b 0.0.0.0:8080 --chdir app app:app
	# Make sure redis is running

make test:
	python3 -m unittest discover .

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis

make docker:
	docker build -t jrsmiffy/ultima . && docker run --name ultima -p 8080:8080 -d jrsmiffy/ultima
