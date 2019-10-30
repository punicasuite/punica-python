SHELL := /bin/bash

venv:
	rm -rf ./venv; \
	python3 -m venv venv; \
	. venv/bin/activate

install:
	. venv/bin/activate; \
	pip3 install -r requirements.txt

install-dev:
	. venv/bin/activate; \
	pip3 install -r requirements-dev.txt

install-dev-mirror:
	. venv/bin/activate; \
	pip3 install -r requirements-dev.txt -i  https://mirrors.aliyun.com/pypi/simple

list:
	. venv/bin/activate; \
	pip3 list --format=columns

test:
	python3 -m unittest discover

build:
	python3 setup.py bdist_wheel --python-tag py3

publish:
	twine upload dist/* -u NashMiao -p %PYPI_PASSWORD
