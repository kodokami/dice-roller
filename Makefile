requirements:
	pip install -U pip setuptools wheel
	pip install -r ./requirements.txt

linter:
	pylint ./dice_roller

test:
	pytest ./dice_roller

install:
	pip install -U .

uninstall:
	pip uninstall dice-roller
