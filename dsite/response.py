# dsite/response.py

class Response:
    """
    Oggetto base di risposta HTTP di DSite.
    """

    def __init__(self, content, status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}

    def set_header(self, key, value):
        """
        Aggiunge o modifica un header HTTP.
        """
        self.headers[key] = value

    def to_http(self):
        """
        Converte la Response in formato HTTP testuale.
        (utile per il server interno DSite)
        """

        status_text = self._status_text(self.status)

        response = f"HTTP/1.1 {self.status} {status_text}\r\n"

        # Headers
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"

        response += "\r\n"
        response += self.content

        return response

    def _status_text(self, code):
        """
        Traduzione base degli status code HTTP.
        """

        statuses = {
            200: "OK",
            201: "Created",
            301: "Moved Permanently",
            302: "Found",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error"
        }

        return statuses.get(code, "OK")
