TOURNEY_FILES=tourney.py `find tourney -iname '*.py'`
ALL_FILES=${TOURNEY_FILES}
MODULES=tourney

install-deps:
	pip install --upgrade pip virtualenv

install-deps-user:
	pip install --user --upgrade pip virtualenv

setup-venv: clean-venv
	virtualenv -p python3 .venv

setup-reqs-venv: clean
	.venv/bin/pip install -r requirements.txt

setup-reqs: clean
	pip install -r requirements.txt

setup: setup-venv setup-reqs-venv

clean:
	find . -iname __pycache__ | xargs rm -fr
	find . -iname '*.pyc' | xargs rm -f

clean-venv:
	rm -fr .venv

dist-clean: clean clean-venv

update-requirements: setup
	pip freeze > requirements.txt

check-style:
	flake8 --ignore E111,E114,E121,E126,E127,E221,E241,E302,E305,W504 \
          --max-line-length 100 --count --show-source ${ALL_FILES}

static-analysis:
	vulture --min-confidence 70 --sort-by-size ${ALL_FILES} .vulture-whitelist.py

check-unused:
	vulture --sort-by-size ${TOURNEY_FILES} .vulture-whitelist.py

security-check:
	bandit -r -s B101 ${MODULES}

check: check-style static-analysis security-check

load-test:
	python3 tourney.py --demo --load-test

test: load-test
