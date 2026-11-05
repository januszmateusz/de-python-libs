#!/usr/bin/env bash
# Sesja 2A: fast-forward vs 3-way merge
source "$(dirname "$0")/_lib.sh"

new_sandbox "02-merge"

# Wspólna historia
echo 'hello' > a.txt
mkdir -p src
printf 'def load():\n    return "v1"\n' > src/load.py
git add . && git commit -q -m "feat: initial load"
printf 'def load():\n    return "v2"\n' > src/load.py
git commit -q -am "feat: load v2"

# feature odchodzi od C2
git switch -q -c feature
printf 'def transform():\n    return "t1"\n' > src/transform.py
git add src/transform.py && git commit -q -m "feat: add transform"

# main idzie dalej niezależnie
git switch -q main
printf 'def load():\n    return "v3"\n' > src/load.py
git commit -q -am "feat: load v3"

# docs odchodzi od AKTUALNEGO main (scenariusz fast-forward)
git switch -q -c docs
printf '# Pipeline\n' > README.md
git add README.md && git commit -q -m "docs: add readme"

git switch -q main
git log --oneline --graph --all