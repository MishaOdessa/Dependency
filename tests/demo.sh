#!/bin/bash
# Demo for stage 1: one valid run, then every invalid case in turn.
# Usage: bash tests/demo.sh   (set PYTHON=python3 if needed)

PYTHON=${PYTHON:-python}
MAIN="$(dirname "$0")/../src/main.py"
URL="https://dl-cdn.alpinelinux.org/alpine/v3.19/main"

run_case() {
    echo "=== $1"
    shift
    echo "\$ main.py $*"
    "$PYTHON" "$MAIN" "$@"
    echo "(exit code: $?)"
    echo
}

run_case "VALID: all parameters are correct" \
    --package nginx --repo "$URL" --version 1.24.0 \
    --output graph.svg --ascii-tree --filter lib

run_case "package is missing" --repo "$URL" --version 1
run_case "package is empty" --package "" --repo "$URL" --version 1
run_case "version is missing" --package nginx --repo "$URL"
run_case "version is empty" --package nginx --repo "$URL" --version ""
run_case "repo is not an http(s) URL" \
    --package nginx --repo ftp://example.org --version 1
run_case "test file does not exist" \
    --package A --repo no_such_file.txt --test-mode --version 1
run_case "output is not .svg" \
    --package nginx --repo "$URL" --version 1 --output pic.png
run_case "unknown option" \
    --package nginx --repo "$URL" --version 1 --color red