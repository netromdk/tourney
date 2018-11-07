#!/bin/sh
FLD="$(cd "$(dirname "$0")" || exit; pwd -P)"
echo "git pulling in ${FLD}.."
git pull -s recursive -X theirs --rebase --autostash
