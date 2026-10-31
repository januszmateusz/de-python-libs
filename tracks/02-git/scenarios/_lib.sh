#!/usr/bin/env bash
# Wspólne helpery dla scenariuszy kursu Git
set -euo pipefail

SANDBOX_ROOT="${SANDBOX_ROOT:-$HOME/git-sandbox}"

new_sandbox() {
  local name="${1:?Podaj nazwę sandboxa}"
  local dir="$SANDBOX_ROOT/$name"

  rm -rf "${dir:?}"
  mkdir -p "$dir"
  cd "$dir"

  git init -q -b main
  git config user.name  "Sandbox User"
  git config user.email "sandbox@example.com"
  # Wyłączamy konwersję CRLF, żeby hashe były przewidywalne (temat na sesję 6)
  git config core.autocrlf false

  echo "Sandbox gotowy: $dir"
}