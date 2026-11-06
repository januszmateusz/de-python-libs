#!/usr/bin/env bash
# Sesja 2C: konflikty w merge i rebase
source "$(dirname "$0")/_lib.sh"

new_sandbox "04-conflict"

cat > config.py <<'EOF'
# source
SOURCE = "s3://raw/flights"

# batching
BATCH_SIZE = 100

# reliability
RETRIES = 3
TIMEOUT = 30
EOF
git add config.py && git commit -q -m "feat: pipeline config"

# feature: F1 zmienia BATCH_SIZE, F2 zmienia TIMEOUT
git switch -q -c feature
sed -i 's/^BATCH_SIZE = 100$/BATCH_SIZE = 1000/' config.py
git commit -q -am "perf: increase batch size to 1000"
sed -i 's/^TIMEOUT = 30$/TIMEOUT = 60/' config.py
git commit -q -am "fix: raise timeout to 60s"

# main: jeden commit zmienia SOURCE i BATCH_SIZE
git switch -q main
sed -i 's#^SOURCE = "s3://raw/flights"$#SOURCE = "s3://raw/flights_v2"#' config.py
sed -i 's/^BATCH_SIZE = 100$/BATCH_SIZE = 500/' config.py
git commit -q -am "feat: switch to flights_v2 source"

git log --oneline --graph --all