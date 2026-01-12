requirements:
	pip install -U pip setuptools wheel
	pip install -r ./requirements.txt

linter:
	python -m pylint ./dice_roller

test:
	python -m pytest ./tests --cov=dice_roller

install:
	pip install -U .

uninstall:
	pip uninstall dice-roller
