all: help

check:
	flake8 application

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

help:
	@echo 'check     -- check the code syntax'
	@echo 'clean     -- cleanup the environment'
	@echo 'help      -- display this information'
	@echo 'httpd     -- start a local development server'
	@echo 'install   -- install all dependencies'
	@echo 'test      -- test the all code'
	@echo 'uninstall -- uninstall all dependencies'

httpd:
	foreman start web -p 8001

test: uninstall clean install check
	py.test

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

uninstall:
	- pip uninstall --yes -r requirements.txt
	- pip uninstall --yes -r requirements-dev.txt
