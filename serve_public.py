#!/usr/bin/env python3
"""Serve the launcher's public copy plus one live, uncached manual-price route."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import os
from pathlib import Path
import stat

MAX_MANUAL_BYTES = 262144
EMPTY_MANUAL = b'{"ar":[],"us":[]}\n'


def read_manual_prices(path):
    """Open the current file afresh, including after an editor's atomic replacement."""
    try:
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            file_fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
        finally:
            os.close(directory_fd)
        with os.fdopen(file_fd, 'rb') as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise PermissionError('Manual price file must be a regular file')
            content = source.read(MAX_MANUAL_BYTES + 1)
    except FileNotFoundError:
        return EMPTY_MANUAL
    if len(content) > MAX_MANUAL_BYTES:
        raise ValueError('Manual price file exceeds 256 KiB')
    return content


def make_handler(public_dir, manual_path):
    public_dir = Path(public_dir).absolute()
    manual_path = Path(manual_path).absolute()

    class PublicHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(public_dir), **kwargs)

        def send_head(self):
            if self.path.partition('?')[0] != '/data/manual-prices.json':
                return super().send_head()
            try:
                content = read_manual_prices(manual_path)
            except OSError:
                self.send_error(403, 'Manual price file is not a readable regular file')
                return None
            except ValueError:
                self.send_error(413, 'Manual price file exceeds 256 KiB')
                return None
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            return BytesIO(content)

    return PublicHandler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', required=True, type=Path)
    parser.add_argument('--port', type=int, default=8792)
    args = parser.parse_args()
    manual_path = Path(__file__).absolute().parent / 'data' / 'manual-prices.json'
    handler = make_handler(args.directory, manual_path)
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
