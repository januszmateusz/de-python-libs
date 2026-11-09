#!/usr/bin/env bash
# Sesja 3A: interactive rebase — brudny feature branch do posprzątania
source "$(dirname "$0")/_lib.sh"

new_sandbox "05-interactive-rebase"

mkdir -p src tests
printf '# Flights pipeline\n' > README.md
git add . && git commit -q -m "chore: init repo"

git switch -q -c feature

# 1. loader z literówką w nazwie funkcji
cat > src/loader.py <<'EOF'
def load_flihgts(path):
    return open(path).read().splitlines()
EOF
git add . && git commit -q -m "add loader"

# 2. początek testów
cat > tests/test_loader.py <<'EOF'
from src.loader import load_flights
EOF
git add . && git commit -q -m "wip"

# 3. poprawka literówki z commita 1
sed -i 's/load_flihgts/load_flights/' src/loader.py
git commit -q -am "fix typo"

# 4. niezależna funkcjonalność
cat > src/aircraft.py <<'EOF'
def aircraft_dim(rows):
    return {r["tail"]: r for r in rows}
EOF
git add . && git commit -q -m "aircraft stuff"

# 5. dokończenie testów
cat >> tests/test_loader.py <<'EOF'

def test_load_flights(tmp_path):
    f = tmp_path / "f.csv"
    f.write_text("a\nb\n")
    assert load_flights(f) == ["a", "b"]
EOF
git commit -q -am "tests"

# 6. debug, który nie powinien trafić do PR
sed -i 's/^    return open/    print("DEBUG", path)\n    return open/' src/loader.py
git commit -q -am "debug print"

git log --oneline --graph --all