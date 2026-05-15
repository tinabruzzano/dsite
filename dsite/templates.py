# dsite/templates.py

import os
import re
from pathlib import Path

BASE_DIR = Path.cwd()


def render_template(template_name, context=None):
    """
    Carica e renderizza un template DSite (XML/HTML).
    """

    if context is None:
        context = {}

    template_path = _resolve_template_path(template_name)

    if not template_path.exists():
        return f"<h1>Template non trovato: {template_name}</h1>"

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Variabili tipo {{ var }}
    content = _render_variables(content, context)

    # 2. Include semplice (futuro expand system)
    content = _render_includes(content)

    return content


def _resolve_template_path(template_name):
    """
    Converte 'app:template.xml' in path reale.
    """

    if ":" in template_name:
        app, file = template_name.split(":")
        return BASE_DIR / app / "pages" / file

    return BASE_DIR / "pages" / template_name


def _render_variables(content, context):
    """
    Sostituisce {{ var }} con valori Python.
    """

    def replace(match):
        key = match.group(1).strip()
        return str(context.get(key, ""))

    return re.sub(r"\{\{\s*(.*?)\s*\}\}", replace, content)


def _render_includes(content):
    """
    Placeholder per sistema future tipo:
    <include file="base.xml" />
    """

    # per ora non fa nulla, ma è pronto per DSite expand system
    return content
