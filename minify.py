#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minification CSS + JS pour Garage Locarno.
Règles sûres (CLAUDE.md) : préserver les espaces dans calc(), ne pas couper les URLs ://."""
import os, re
ROOT = os.path.dirname(os.path.abspath(__file__))

# --- CSS ---
with open(os.path.join(ROOT, "css/style.css"), encoding="utf-8") as f:
    css = f.read()
css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)   # commentaires
css = re.sub(r'[ \t]+', ' ', css)                       # espaces multiples
css = re.sub(r'\s*([{};:,>~])\s*', r'\1', css)          # autour des séparateurs
css = re.sub(r'\s*\{\s*', '{', css)
css = re.sub(r';\}', '}', css)
css = re.sub(r'\n+', '', css)
# Note : les espaces simples autour de + et - dans calc() sont préservés
# (ni + ni - ne figurent dans la classe de séparateurs ci-dessus).
css = css.strip()
with open(os.path.join(ROOT, "css/style.min.css"), "w", encoding="utf-8") as f:
    f.write(css)
print("css/style.min.css", len(css), "o")

# --- JS ---
# Minification volontairement conservatrice : on ne supprime QUE les
# commentaires de ligne entière (la ligne ne contient que `// ...`) et les
# blocs /* ... */. On ne touche jamais à un `//` en milieu de ligne, pour ne
# pas casser une URL (://) ni un littéral regex comme /^\.\.\//.
with open(os.path.join(ROOT, "js/main.js"), encoding="utf-8") as f:
    lines = f.read().split("\n")
cleaned = [line.rstrip() for line in lines if not line.strip().startswith("//")]
js = "\n".join(cleaned)
js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)  # commentaires bloc
js = "\n".join(l for l in js.split("\n") if l.strip())
with open(os.path.join(ROOT, "js/main.min.js"), "w", encoding="utf-8") as f:
    f.write(js)
print("js/main.min.js", len(js), "o")
