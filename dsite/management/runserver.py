# dsite/management/runserver.py

from http.server import HTTPServer, BaseHTTPRequestHandler
from dsite.template import render_template


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        content = render_template("homepage.xml")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(content.encode("utf-8"))


def runserver(project_name):

    print(f"[DSite] Server avviato per {project_name}")
    print("[DSite] http://127.0.0.1:8000")

    server = HTTPServer(("127.0.0.1", 8000), Handler)
    server.serve_forever()
