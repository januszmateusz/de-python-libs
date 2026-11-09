#!/usr/bin/env bash
# Sesja 3B: amend, fixup/autosquash, squash merge
source "$(dirname "$0")/_lib.sh"

new_sandbox "06-history-polish"

mkdir -p src tests
printf '# Flights pipeline\n' > README.md
git add . && git commit -q -m "chore: init repo"

git switch -q -c feature

cat > src/loader.py <<'EOF'
def load_flights(path):
    return open(path).read().splitlines()
EOF
git add . && git commit -q -m "feat(loader): add flights loader"

cat > tests/test_loader.py <<'EOF'
from src.loader import load_flights


def test_load(tmp_path):
    f = tmp_path / "f.csv"
    f.write_text("a\nb\n")
    assert load_flights(f) == ["a", "b"]
EOF
git add . && git commit -q -m "test(loader): add loader tests"

cat > src/aircraft.py <<'EOF'
def aircraft_dim(rows):
    return {r["tail"]: r for r in rows}
EOF
git add src/aircraft.py && git commit -q -m "feat(dim): add aircraft dimension"

# "zapomniany" plik — nieśledzony, do ćwiczenia z amend
touch src/__init__.py

git log --oneline --graph --all
git status --short