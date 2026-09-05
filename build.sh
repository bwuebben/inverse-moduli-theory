#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir/paper"

command -v latexmk >/dev/null 2>&1 || {
  echo "Error: latexmk is not installed or not on PATH." >&2
  exit 127
}

latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf inverse-moduli-theory.pdf
echo "Built $script_dir/paper/inverse-moduli-theory.pdf"
