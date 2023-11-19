requirements:
	pip install -U pip setuptools wheel
	pip install -r ./requirements.txt

linter:
	pylint ./dice_roller
