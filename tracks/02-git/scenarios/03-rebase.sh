#!/usr/bin/env bash
# Sesja 2B: rebase bez konfliktów
source "$(dirname "$0")/_lib.sh"

new_sandbox "03-rebase"

# Wspólna historia
echo 'hello' > a.txt
mkdir -p src
printf 'def load():\n    return "v1"\n' > src/load.py
git add . && git commit -q -m "feat: initial load"
printf 'def load():\n    return "v2"\n' > src/load.py
git commit -q -am "feat: load v2"

# feature: dwa commity na transform.py
git switch -q -c feature
printf 'def transform():\n    return "t1"\n' > src/transform.py
git add src/transform.py && git commit -q -m "feat: add transform"
printf 'def transform():\n    return "t2"\n' > src/transform.py
git commit -q -am "feat: transform v2"

# main: dwa commity w innych plikach
git switch -q main
printf 'def load():\n    return "v3"\n' > src/load.py
git commit -q -am "feat: load v3"
printf '# Pipeline\n' > README.md
git add README.md && git commit -q -m "docs: add readme"

# Startujemy na feature
git switch -q feature
git log --oneline --graph --all