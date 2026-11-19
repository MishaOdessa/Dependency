#!/bin/bash
# Demo for stages 1-2: valid runs first, then every error case in turn.
# Usage: bash tests/demo.sh   (set PYTHON=python3 if needed)

PYTHON=${PYTHON:-python}
MAIN="$(dirname "$0")/../src/main.py"
URL=${URL:-https://dl-cdn.alpinelinux.org/alpine/v3.19/main}

run_case() {
    echo "=== $1"
    shift
    echo "\$ main.py $*"
    "$PYTHON" "$MAIN" "$@"
    echo "(exit code: $?)"
    echo
}

# --- valid runs: direct dependencies are printed
run_case "VALID: package with one dependency" \
    --package busybox --repo "$URL" --version 1.36.1
run_case "VALID: package with several dependencies" \
    --package curl --repo "$URL" --version 8.14.1
run_case "VALID: exact version with release suffix" \
    --package curl --repo "$URL" --version 8.14.1-r2

# --- stage 2 errors: data collection
run_case "package not found in the index" \
    --package no-such-package --repo "$URL" --version 1
run_case "version not found in the index" \
    --package curl --repo "$URL" --version 9.9.9
run_case "repository has no index (404)" \
    --package curl --repo "$URL/no-such-dir" --version 1
run_case "test mode is not supported yet" \
    --package A --repo "$0" --test-mode --version 1

# --- stage 1 errors: parameter validation
run_case "package is missing" --repo "$URL" --version 1
run_case "package is empty" --package "" --repo "$URL" --version 1
run_case "version is missing" --package curl --repo "$URL"
run_case "version is empty" --package curl --repo "$URL" --version ""
run_case "repo is not an http(s) URL" \
    --package curl --repo ftp://example.org --version 1
run_case "test file does not exist" \
    --package A --repo no_such_file.txt --test-mode --version 1
run_case "output is not .svg" \
    --package curl --repo "$URL" --version 1 --output pic.png
run_case "unknown option" \
    --package curl --repo "$URL" --version 1 --color red