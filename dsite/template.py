# dsite/template.py

import os
import re
import io
import contextlib


BASE_DIR = os.getcwd()


# =========================================
# TEMPLATE RENDER
# =========================================

def render_template(template_name, context=None):
    """
    Render principale DSite.
    Supporta:
    - <expand />
    - <file-html />
    - <html-block>
    - <pyfunct>
    - <pycontent>
    - <add-base-classification />
    - {{ variables }}
    """

    if context is None:
        context = {}

    path = _resolve(template_name)

    if not os.path.exists(path):
        return f"<h1>Template non trovato: {template_name}</h1>"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # -----------------------------
    # VARIABLES
    # -----------------------------
    content = _render_variables(content, context)

    # -----------------------------
    # EXPAND SYSTEM
    # -----------------------------
    content = _render_expand(content)

    # -----------------------------
    # HTML BLOCK
    # -----------------------------
    content = _render_html_blocks(content)

    # -----------------------------
    # PYFUNCT
    # -----------------------------
    content = _render_pyfunct(content)

    # -----------------------------
    # BASE CLASSIFICATION
    # -----------------------------
    content = _render_base_classification(content)

    return content


# =========================================
# PATH RESOLVE
# =========================================

def _resolve(name):

    if ":" in name:
        app, file = name.split(":")
        return os.path.join(BASE_DIR, app, "pages", file)

    return os.path.join(BASE_DIR, "pages", name)


# =========================================
# VARIABLES {{ var }}
# =========================================

def _render_variables(content, context):

    def replace(match):
        key = match.group(1).strip()
        return str(context.get(key, ""))

    return re.sub(
        r"\{\{\s*(.*?)\s*\}\}",
        replace,
        content
    )


# =========================================
# EXPAND
# =========================================

def _render_expand(content):

    pattern = r'<expand file="(.*?)"\s*/>'

    match = re.search(pattern, content)

    if not match:
        return content

    base_file = match.group(1)

    base_path = _resolve(base_file)

    if not os.path.exists(base_path):
        return content

    with open(base_path, "r", encoding="utf-8") as f:
        base_content = f.read()

    # remove expand tag
    page_content = re.sub(pattern, "", content).strip()

    # insert inside <file-html />
    base_content = base_content.replace(
        "<file-html />",
        page_content
    )

    return base_content


# =========================================
# HTML BLOCK
# =========================================

def _render_html_blocks(content):

    pattern = r"<html-block>(.*?)</html-block>"

    def replace(match):
        return match.group(1).strip()

    return re.sub(
        pattern,
        replace,
        content,
        flags=re.DOTALL
    )


# =========================================
# BASE CLASSIFICATION
# =========================================

def _render_base_classification(content):

    base_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DSite</title>
</head>
<body>

[file-html]

</body>
</html>
"""

    if "<add-base-classification />" not in content:
        return content

    content = content.replace(
        "<add-base-classification />",
        ""
    )

    return base_html.replace(
        "[file-html]",
        content
    )


# =========================================
# PYFUNCT
# =========================================

def _render_pyfunct(content):

    pattern = r"<pyfunct>\s*<pycontent>(.*?)</pycontent>\s*</pyfunct>"

    def replace(match):

        code = match.group(1).strip()

        # -----------------------------
        # SECURITY CHECK
        # -----------------------------

        blocked = [
            "import",
            "open(",
            "exec(",
            "eval(",
            "__import__",
            "os.",
            "sys.",
            "subprocess",
            "socket",
            "shutil",
            "pathlib",
            "compile(",
            "globals(",
            "locals(",
            "vars(",
            "input(",
        ]

        for item in blocked:
            if item in code:
                return (
                    "<h3>"
                    "DSite SecurityError: "
                    f"'{item}' non consentito."
                    "</h3>"
                )

        # -----------------------------
        # SAFE BUILTINS
        # -----------------------------

        safe_builtins = {
            "print": print,
            "range": range,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
        }

        safe_globals = {
            "__builtins__": safe_builtins
        }

        buffer = io.StringIO()

        try:

            with contextlib.redirect_stdout(buffer):
                exec(code, safe_globals, {})

            return buffer.getvalue()

        except Exception as e:

            return (
                "<h3>"
                f"DSite PyFunct Error: {e}"
                "</h3>"
            )

    return re.sub(
        pattern,
        replace,
        content,
        flags=re.DOTALL
    )
