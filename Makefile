install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	#format code
	black *.py pages/*.py
lint:
	#flake8 or #pylint
	# pylint --disable=R,C *.py pages/*.py
test:
	#test
	# python -m pytest -vv --cov=mylib test_logic.py
build:
	#build container
	# docker build -t deploy-fastapi .
run:
	#run docker
	#docker run -p 127.0.0.1:8080:8080 ff3b59fc449b
deploy:
	#deploy

all: install lint  