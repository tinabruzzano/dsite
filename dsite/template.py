# dsite/template.py

import os
import re

BASE_DIR = os.getcwd()


def render_template(template_name, context=None):
    if context is None:
        context = {}

    path = _resolve(template_name)

    if not os.path.exists(path):
        return f"<h1>Template non trovato: {template_name}</h1>"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = _variables(content, context)
    content = _expand(content)

    return content


def _resolve(name):
    if ":" in name:
        app, file = name.split(":")
        return os.path.join(BASE_DIR, app, "pages", file)

    return os.path.join(BASE_DIR, "pages", name)


def _variables(content, context):
    return re.sub(
        r"\{\{\s*(.*?)\s*\}\}",
        lambda m: str(context.get(m.group(1), "")),
        content
    )


def _expand(content):
    # <expand file="base.xml" />
    pattern = r'<expand file="(.*?)"\s*/>'

    def replace(match):
        file = match.group(1)
        path = _resolve(file)

        if not os.path.exists(path):
            return ""

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return re.sub(pattern, replace, content)
