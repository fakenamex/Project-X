from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .config import SETTINGS
from .orchestrator import AutonomousNewsroom
from .repository import Repository


class App:
    def __init__(self) -> None:
        self.repository = Repository(SETTINGS.db_path)
        self.newsroom = AutonomousNewsroom(SETTINGS, self.repository)
        self.newsroom.start()


def create_app() -> App:
    return App()


def run_server() -> None:
    app = create_app()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/api/articles":
                articles = app.repository.list_recent_articles(limit=20)
                payload = [
                    {
                        "id": a.id,
                        "title": a.title,
                        "body": a.body,
                        "category": a.category,
                        "published_at": a.published_at.isoformat(),
                    }
                    for a in articles
                ]
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
                return

            if self.path == "/":
                articles = app.repository.list_recent_articles(limit=10)
                cards = "".join(
                    f"<article><h3>{a.title}</h3><p>{a.body}</p><small>{a.published_at}</small></article>"
                    for a in articles
                )
                html = f"""
                <html><head><meta charset='utf-8'><title>Project-X Newsroom</title></head>
                <body>
                  <h1>KI Newsroom (DE)</h1>
                  <p>Autonome tägliche Analyse deutscher Nachrichten.</p>
                  {cards or '<p>Noch keine Artikel vorhanden. Erste Tagesrunde läuft…</p>'}
                </body></html>
                """
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
                return

            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer((SETTINGS.host, SETTINGS.port), Handler)
    try:
        server.serve_forever()
    finally:
        app.newsroom.stop()
        server.server_close()
