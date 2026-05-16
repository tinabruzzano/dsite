# dsite/template.py

import os
import re
import io
import secrets
import contextlib


BASE_DIR = os.getcwd()


# =========================================
# MAIN TEMPLATE RENDER
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
    - <form-token />
    - {{ variables }}
    """

    if context is None:
        context = {}

    # ---------------------------------
    # TEMPLATE PATH
    # ---------------------------------

    path = _resolve(template_name)

    if not os.path.exists(path):

        return (
            "<h1>"
            f"DSite TemplateError: "
            f"template '{template_name}' non trovato."
            "</h1>"
        )

    # ---------------------------------
    # LOAD FILE
    # ---------------------------------

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # ---------------------------------
    # VARIABLES
    # ---------------------------------

    content = _render_variables(content, context)

    # ---------------------------------
    # EXPAND
    # ---------------------------------

    content = _render_expand(content)

    # ---------------------------------
    # HTML BLOCK
    # ---------------------------------

    content = _render_html_blocks(content)

    # ---------------------------------
    # PYFUNCT
    # ---------------------------------

    content = _render_pyfunct(content)

    # ---------------------------------
    # FORM TOKENS
    # ---------------------------------

    content = _render_form_tokens(content)

    # ---------------------------------
    # BASE CLASSIFICATION
    # ---------------------------------

    content = _render_base_classification(content)

    return content


# =========================================
# PATH RESOLVE
# =========================================

def _resolve(name):

    # app:file.xml

    if ":" in name:

        app, file = name.split(":")

        return os.path.join(
            BASE_DIR,
            app,
            "pages",
            file
        )

    # pages/file.xml

    return os.path.join(
        BASE_DIR,
        "pages",
        name
    )


# =========================================
# VARIABLES {{ }}
# =========================================

def _render_variables(content, context):

    pattern = r"\{\{\s*(.*?)\s*\}\}"

    def replace(match):

        key = match.group(1).strip()

        return str(
            context.get(key, "")
        )

    return re.sub(
        pattern,
        replace,
        content
    )


# =========================================
# EXPAND SYSTEM
# =========================================

def _render_expand(content):

    pattern = r'<expand file="(.*?)"\s*/>'

    match = re.search(pattern, content)

    if not match:
        return content

    base_file = match.group(1)

    base_path = _resolve(base_file)

    if not os.path.exists(base_path):

        return (
            "<h1>"
            f"DSite ExpandError: "
            f"base file '{base_file}' non trovato."
            "</h1>"
        )

    with open(base_path, "r", encoding="utf-8") as f:
        base_content = f.read()

    # remove expand tag

    page_content = re.sub(
        pattern,
        "",
        content
    ).strip()

    # insert into <file-html />

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

    if "<add-base-classification />" not in content:
        return content

    base_html = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"
>

<title>DSite</title>

</head>
<body>

[file-html]

</body>
</html>
"""

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

        # ---------------------------------
        # BLOCKED CODE
        # ---------------------------------

        blocked = [

            # imports
            "import",

            # dangerous builtins
            "open(",
            "exec(",
            "eval(",
            "compile(",
            "__import__",

            # system access
            "os.",
            "sys.",
            "subprocess",
            "socket",
            "pathlib",
            "shutil",

            # env access
            "globals(",
            "locals(",
            "vars(",

            # interaction
            "input(",

            # loops abuse
            "while True",

        ]

        for item in blocked:

            if item in code:

                return (
                    "<h3>"
                    "DSite SecurityError: "
                    f"'{item}' non consentito."
                    "</h3>"
                )

        # ---------------------------------
        # SAFE BUILTINS
        # ---------------------------------

        safe_builtins = {

            "print": print,

            "range": range,

            "len": len,

            "str": str,
            "int": int,
            "float": float,

            "list": list,
            "dict": dict,
            "tuple": tuple,

            "min": min,
            "max": max,
            "sum": sum,

            "abs": abs,

        }

        safe_globals = {
            "__builtins__": safe_builtins
        }

        buffer = io.StringIO()

        try:

            with contextlib.redirect_stdout(buffer):

                exec(
                    code,
                    safe_globals,
                    {}
                )

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


# =========================================
# FORM TOKEN
# =========================================

def _render_form_tokens(content):

    pattern = r'<form-token type="(.*?)"\s*/>'

    allowed_types = {

        "ea": "Edit App",

        "eug": "Edit Users and/or Groups"

    }

    def replace(match):

        token_type = match.group(1)

        # ---------------------------------
        # INVALID TYPE
        # ---------------------------------

        if token_type not in allowed_types:

            return (
                "<h3>"
                "DSite FormTokenError: "
                f"tipo '{token_type}' non valido."
                "</h3>"
            )

        # ---------------------------------
        # TOKEN
        # ---------------------------------

        token = secrets.token_hex(32)

        return f'''
<input
type="hidden"
name="_dsite_token"
value="{token}"
data-type="{token_type}"
>
'''

    return re.sub(
        pattern,
        replace,
        content
    )
