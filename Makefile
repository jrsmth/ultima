make start:
	sass --update static/styles/scss:static/styles/css && flask run

make test:
	python3 -m unittest test

make redis:
	docker run --name ultima-redis -p 6379:6379 -d redis