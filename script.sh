#!/usr/bin/env bash
ARGS=$1

COMMIT_MSG=`head -n1 $ARGS`
PATTERN="^(CDD|CDTS)-[0-9]+[[:space:]]-[[:space:]]"
if ! [[ "$COMMIT_MSG" =~ $PATTERN ]]; then
  echo "Bad commit message '$COMMIT_MSG'. It must be in the format of 'CDD-1234 - message here' or 'CDTS-1234 - message here'"
  exit 1
fi
