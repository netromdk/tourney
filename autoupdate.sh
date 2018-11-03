#!/bin/sh
echo "Tourney is auto-updating.."

./update.sh

echo "Starting tourney.py again.."
./tourney.py
