make start:
	sass --update static/styles/scss:static/styles/css && flask run

make test:
	python3 -m unittest test