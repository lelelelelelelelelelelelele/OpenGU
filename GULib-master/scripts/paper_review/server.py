"""Loopback-only review service. Run: python -m scripts.paper_review.server."""
import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import secrets
import subprocess
from urllib.parse import urlparse, parse_qs, unquote

from .model import BLOCKS, Desk
from .render import render
from .sync import Cloud


def make_server(desk, port):
    token = secrets.token_urlsafe(32)
    cloud = Cloud(desk)
    assets = Path(__file__).parent / 'web'

    class Handler(BaseHTTPRequestHandler):
        def send(self, data, content='application/json; charset=utf-8', status=200):
            if not isinstance(data, bytes):
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if self.path.startswith('/preview/'):
                self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self'; font-src 'self'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(data)

        def allowed(self):
            return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

        def do_GET(self):
            if not self.allowed():
                return self.send({'error': '不接受此 Host。'}, status=403)
            parsed = urlparse(self.path)
            path = parsed.path
            try:
                if path == '/api/state':
                    return self.send(dict(token=token, blocks=[desk.block(k) for k in BLOCKS], cloud=cloud.status()))
                if path == '/api/block':
                    key = parse_qs(parsed.query)['id'][0]
                    return self.send(dict(block=desk.block(key), events=desk.events(key), diff=desk.git_diff()))
                if path == '/api/package':
                    return self.send(cloud.package(), 'application/zip')
                if path == '/api/preview':
                    key = parse_qs(parsed.query)['id'][0]
                    document = render(desk, key)
                    return self.send(dict(url='/preview/' + document.relative_to(desk.state / 'html-preview').as_posix()))
                if path.startswith('/preview/'):
                    root = desk.state / 'html-preview'
                    target = (root / unquote(path.removeprefix('/preview/'))).resolve()
                    if not target.is_relative_to(root) or target.suffix not in {'.html', '.css', '.svg'}:
                        raise ValueError('无效预览路径。')
                    return self.send(target.read_bytes(), mimetypes.guess_type(target)[0] + '; charset=utf-8')
                if path.startswith('/paper/'):
                    target = (desk.paper / unquote(path.removeprefix('/paper/'))).resolve()
                    if not target.is_relative_to(desk.paper / 'figures') or target.suffix != '.pdf':
                        raise ValueError('无效图文件路径。')
                    return self.send(target.read_bytes(), 'application/pdf')
                if path in {'/', '/app.js', '/style.css', '/reader.css'}:
                    target = assets / ('index.html' if path == '/' else path[1:])
                    return self.send(target.read_bytes(), mimetypes.guess_type(target)[0] + '; charset=utf-8')
                self.send({'error': '页面不存在。'}, status=404)
            except (KeyError, ValueError, OSError, RuntimeError, subprocess.SubprocessError) as error:
                self.send({'error': str(error)}, status=400)

        def do_POST(self):
            origin = self.headers.get('Origin')
            expected = f'http://127.0.0.1:{self.server.server_port}'
            if not self.allowed() or self.headers.get('X-Review-Token') != token or origin not in {None, expected}:
                return self.send({'error': '请求来源无效，请刷新页面。'}, status=403)
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 30_000_000:
                    raise ValueError('请求为空或超过 30 MB。')
                raw = self.rfile.read(length)
                if self.path == '/api/cloud/check':
                    return self.send(cloud.check(raw))
                payload = json.loads(raw)
                if self.path == '/api/cloud/pull':
                    return self.send(cloud.pull())
                key = payload.get('id')
                if self.path == '/api/save':
                    return self.send(desk.save(key, payload['version'], payload['source'], payload['reason']))
                if self.path == '/api/comment':
                    desk.comment(key, payload['version'], payload['text'])
                    return self.send({'ok': True})
                return self.send({'error': '接口不存在。'}, status=404)
            except (KeyError, ValueError, OSError) as error:
                self.send({'error': str(error)}, status=409)

    return HTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper', type=Path, default=Path(__file__).resolve().parents[2] / 'report/paper/overleaf')
    parser.add_argument('--state-dir', type=Path, required=True, help='Durable local review history and cloud receipts; keep outside manuscript sources.')
    parser.add_argument('--port', type=int, default=8129)
    args = parser.parse_args()
    desk = Desk(args.paper, args.state_dir)
    server = make_server(desk, args.port)
    print(f'Review desk: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
