make build:
	sass --update static/styles/scss:static/styles/css

make start:
	make build && gunicorn app:app
	# Make sure redis is running

make test:
	python3 -m unittest test

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis