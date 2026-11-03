#!/usr/bin/env bash
# Sesja 1: obiekty, snapshoty, DAG
source "$(dirname "$0")/_lib.sh"

new_sandbox "01-object-model"

# Ćw. 1–2: dwa identyczne pliki + src/load.py v1, pierwszy commit
echo 'hello' > a.txt
echo 'hello' > b.txt
mkdir -p src
printf 'def load():\n    return "v1"\n' > src/load.py
git add a.txt b.txt src/load.py
git commit -q -m "feat: initial load"

# Ćw. 3: zmiana tylko src/load.py, drugi commit
printf 'def load():\n    return "v2"\n' > src/load.py
git commit -q -am "feat: load v2"

# Kontrola stanu końcowego części A
objects=$(find .git/objects -type f | wc -l)
echo "Commity:"
git log --oneline
echo "Obiekty w .git/objects: $objects (oczekiwane: 9)"