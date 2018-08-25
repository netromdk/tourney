#!/bin/sh
echo "Tourney is auto-updating.."

echo "git pulling.."
git pull --rebase --autostash

echo "Starting tourney.py again.."
./tourney.py
