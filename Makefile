.PHONY: build

install:
	pip install --user pipenv
	pipenv install
	pipenv shell

install-dev:
	pip install --user pipenv
	pipenv install --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	pipenv shell

install-mirror:
	pip install --user pipenv
	pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	pipenv shell

test:
	python -m unittest discover

build:
	python setup.py bdist_wheel --python-tag py3

publish:
	twine upload dist/* -u NashMiao -p %PYPI_PASSWORD
