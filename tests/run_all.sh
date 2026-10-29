#!/usr/bin/env bash
# Maintainer test: run every example once against the live Actors through the local CLI proxy.
# Needs: `apify login` done, Python venv with requirements.txt, `npm install`. Costs a few cents in total.
# Usage: PYTHON=/path/to/venv/bin/python tests/run_all.sh [port]
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
PORT="${1:-8799}"; PY="${PYTHON:-python3}"
export EXAMPLES_PROXY_URL="http://127.0.0.1:${PORT}" APIFY_TOKEN="not-a-real-token-tests-use-cli-proxy"
python3 tests/apify_cli_proxy.py "$PORT" > /tmp/apify-examples-proxy.log 2>&1 & PROXY_PID=$!
trap 'kill $PROXY_PID 2>/dev/null' EXIT; sleep 1
pass=0; fail=0
check() { local dir="$1" name="$2"; shift 2; echo "=== $dir/$name"; if (cd "$dir" && "$@") > "/tmp/ex-$dir-$name.log" 2>&1; then pass=$((pass+1)); echo "PASS"; else fail=$((fail+1)); echo "FAIL (see /tmp/ex-$dir-$name.log)"; fi; tail -n 6 "/tmp/ex-$dir-$name.log"; }
for f in $(ls */*.py | grep -v ^tests/); do d=$(dirname "$f"); n=$(basename "$f"); check "$d" "$n" "$PY" ../tests/patch_python.py "$n"; done
for f in $(ls */*.mjs | grep -v ^tests/); do d=$(dirname "$f"); n=$(basename "$f"); check "$d" "$n" node --import ../tests/js_loader.mjs "$n"; done
for f in */curl.sh; do d=$(dirname "$f"); tmp="/tmp/ex-$d-curl.sh"; sed "s#https://api.apify.com#${EXAMPLES_PROXY_URL}#g" "$f" > "$tmp"; check "$d" curl.sh bash "$tmp"; done
echo "passed $pass, failed $fail"; [ "$fail" -eq 0 ]
