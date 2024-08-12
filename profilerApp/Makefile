install:
	.venv\Scripts\activate \
	pip install --upgrade pip &&\
	pip install -r requirements.txt

make_vm:
	python -m venv venv

test:
	python -m pytest	

dockstyle:
	pydocstyle ./src run.py

lint:
	pylint --disable=C0303 run.py ./src

clean: test lint dockstyle

