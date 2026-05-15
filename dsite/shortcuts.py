
from .templates import render_template
from .response import Response


def render(request, template_name, context=None):
    if context is None:
        context = {}

    html = render_template(template_name, context)
    return Response(html)
