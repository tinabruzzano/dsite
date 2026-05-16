from http.server import HTTPServer, BaseHTTPRequestHandler

from dsite.http.router import resolve
from dsite.http.request import Request
from dsite.template import render_template


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        view = resolve(self.path)

        if view is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        request = Request("GET", self.path)

        response = view(request)

        content = render_template(
            response.content if hasattr(response, "content") else response
        )

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(content.encode("utf-8"))


def runserver(project_name):

    print(f"[DSite] Server avviato ({project_name})")
    print("[DSite] http://127.0.0.1:8000")

    server = HTTPServer(("127.0.0.1", 8000), Handler)
    server.serve_forever()
