.PHONY: build

install:
	pip install --user pipenv
	pipenv install
	pipenv shell

install-mirror:
	pip install --user pipenv
	pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	pipenv shell

test:
	pipenv shell
	python -m unittest discover

build:
	pipenv shell
	pipenv install wheel --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	python setup.py bdist_wheel --python-tag py3

publish:
	pipenv shell
	pipenv install twine --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	twine upload dist/* -u NashMiao -p %PYPI_PASSWORD
