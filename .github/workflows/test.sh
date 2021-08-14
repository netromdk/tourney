#!/bin/bash

setup() {
  make install-deps setup-venv
  source .venv/bin/activate
  make setup-reqs
}

# # Even if .venv is found, make sure required executables are found, otherwise setup anyway.
if [[ ! -d .venv ]]; then
  setup
else
  source .venv/bin/activate
fi

make test
make check
