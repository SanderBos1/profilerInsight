install:
	.venv\Scripts\activate \
	pip install --upgrade pip &&\
	pip install -r requirements.txt

make_vm:
	python -m venv venv

test:
	python	-m	pytest	

lint:
	pylint  --disable=C0303 run.py ./src


all: install lint test
