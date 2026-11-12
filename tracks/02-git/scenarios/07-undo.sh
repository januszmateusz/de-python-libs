#!/usr/bin/env bash
# Sesja 4: cofanie zmian — wspólny scenariusz dla wszystkich bloków
source "$(dirname "$0")/_lib.sh"

new_sandbox "07-undo"

mkdir -p src
printf '# Flights pipeline\n' > README.md
git add . && git commit -q -m "chore: init repo"

cat > src/loader.py <<'EOF'
def load_flights(path):
    return open(path, encoding="utf-8").read().splitlines()
EOF
git add . && git commit -q -m "feat(loader): add flights loader"

cat > src/transform.py <<'EOF'
def clean(rows):
    return [r.strip() for r in rows]
EOF
git add . && git commit -q -m "feat(transform): add clean step"

cat >> src/transform.py <<'EOF'


def dedupe(rows):
    return list(dict.fromkeys(rows))
EOF
git commit -q -am "feat(transform): add dedupe step"

git log --oneline --graph --all