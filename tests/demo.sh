#!/bin/bash
# Demo for stage 3: test repository cases (BFS, cycles, filter), real repo, and errors.

PYTHON=${PYTHON:-python}
MAIN="$(dirname "$0")/../src/main.py"
TEST_REPO="$(dirname "$0")/test_repo.txt"
URL=${URL:-https://dl-cdn.alpinelinux.org/alpine/v3.19/main}

run_case() {
    echo "=== $1"
    shift
    echo "\$ main.py $*"
    "$PYTHON" "$MAIN" "$@"
    echo "(exit code: $?)"
    echo
}

# --- test mode: various graph cases
run_case "TEST MODE: full BFS graph with cycle (B -> D -> B) and diamond (E)" \
    --package A --repo "$TEST_REPO" --test-mode --version 1

run_case "TEST MODE: start directly inside a cycle (package D)" \
    --package D --repo "$TEST_REPO" --test-mode --version 1

run_case "TEST MODE: leaf package without dependencies (package E)" \
    --package E --repo "$TEST_REPO" --test-mode --version 1

run_case "TEST MODE: filter substring (--filter E)" \
    --package A --repo "$TEST_REPO" --test-mode --version 1 --filter E

run_case "TEST MODE: filter root package (--filter A -> empty graph)" \
    --package A --repo "$TEST_REPO" --test-mode --version 1 --filter A

run_case "TEST MODE ERROR: package not found in test file" \
    --package Z --repo "$TEST_REPO" --test-mode --version 1

# --- real repository mode
run_case "REAL REPO: transitive graph for busybox" \
    --package busybox --repo "$URL" --version 1.36.1

run_case "REAL REPO: transitive graph for curl without 'so:' libraries" \
    --package curl --repo "$URL" --version 8.14.1 --filter "so:"

# --- parameter validation errors
run_case "ERROR: test file does not exist" \
    --package A --repo no_such_file.txt --test-mode --version 1

run_case "ERROR: repo is not an http(s) URL" \
    --package curl --repo ftp://example.org --version 1

run_case "ERROR: output is not .svg" \
    --package curl --repo "$URL" --version 1 --output pic.png
