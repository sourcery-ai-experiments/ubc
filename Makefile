install:
	bash install.sh

link:
	lygadgets_link lygadgets
	lygadgets_link tech/ubc

test:
	pytest

test-force:
	pytest --force-regen

cov:
	pytest --cov=ubc

annotations:
	pip install pytest-monkeytype
	py.test --monkeytype-output=./monkeytype.sqlite3
	fish add_types.fish

mypy:
	mypy . --ignore-missing-imports

lint:
	flake8 .

pylint:
	pylint .

lintd2:
	flake8 --select RST

lintd:
	pydocstyle .

doc8:
	doc8 docs/
