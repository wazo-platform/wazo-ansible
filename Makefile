.PHONY:
venv:
	virtualenv -p python3 venv --no-site-packages

.PHONY: setup
setup:
	pip install -r requirements.txt
