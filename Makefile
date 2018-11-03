TOURNEY_FILES=tourney.py `find tourney -iname '*.py'`
ALL_FILES=${TOURNEY_FILES}
MODULES=tourney

setup: clean
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements.txt
	echo "\nTo use environment: source .venv/bin/activate"

clean:
	rm -fr .venv
	find . -iname '*.pyc' | xargs rm -f
	find . -iname __pycache__ | xargs rm -fr

update-requirements: setup
	.venv/bin/pip freeze > requirements.txt

check-style:
	.venv/bin/flake8 --ignore E111,E114,E121,E126,E127,E221,E241,E302,E305 \
          --max-line-length 100 --count --show-source ${ALL_FILES}

static-analysis:
	.venv/bin/vulture --min-confidence 70 --sort-by-size ${ALL_FILES} .vulture-whitelist.py

check-unused:
	.venv/bin/vulture --sort-by-size ${TOURNEY_FILES} .vulture-whitelist.py

security-check:
	.venv/bin/bandit -r -s B101 ${MODULES}

check: check-style static-analysis security-check

load-test:
	.venv/bin/python3 tourney.py --demo --load-test

test: load-test
