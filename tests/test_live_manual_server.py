"""Targeted HTTP-handler checks using in-memory connections; no browser or listener."""
from contextlib import redirect_stderr
from io import BytesIO, StringIO
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from serve_public import EMPTY_MANUAL, MAX_MANUAL_BYTES, make_handler


class Connection:
    def __init__(self, request):
        self.request = BytesIO(request)
        self.response = bytearray()

    def makefile(self, *_args, **_kwargs):
        return self.request

    def sendall(self, data):
        self.response.extend(data)


class LiveManualServer(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.public = self.root / 'public'
        self.public.mkdir()
        (self.public / 'index.html').write_text('Public atlas')
        self.data = self.root / 'project' / 'data'
        self.data.mkdir(parents=True)
        self.manual = self.data / 'manual-prices.json'
        self.manual.write_bytes(EMPTY_MANUAL)
        self.handler = make_handler(self.public, self.manual)

    def request(self, target='/data/manual-prices.json', method='GET', headers=None):
        fields = {'Host':'localhost', 'Connection':'close', **(headers or {})}
        raw = f'{method} {target} HTTP/1.1\r\n' + ''.join(f'{k}: {v}\r\n' for k,v in fields.items()) + '\r\n'
        connection = Connection(raw.encode('ascii'))
        with redirect_stderr(StringIO()):
            self.handler(connection, ('127.0.0.1',12345), SimpleNamespace(server_name='localhost',server_port=8792))
        head, _, body = bytes(connection.response).partition(b'\r\n\r\n')
        lines = head.decode('iso-8859-1').split('\r\n')
        response_headers = {key.lower():value.strip() for key,value in (line.split(':',1) for line in lines[1:])}
        return int(lines[0].split()[1]), response_headers, body

    def test_reload_reads_saved_and_atomically_replaced_file_with_no_cache(self):
        status, headers, first = self.request()
        self.assertEqual(status,200)
        self.assertEqual(first,EMPTY_MANUAL)
        self.assertEqual(headers['cache-control'],'no-store')
        quote = {'ar':[{'date':'2026-10-15','item':'Pecho','machine_name':'pecho','price':18500,'currency':'ARS','unit':'kg'}],'us':[]}
        self.manual.write_text(json.dumps(quote))
        status, _, updated = self.request()
        self.assertEqual(status,200)
        self.assertEqual(json.loads(updated),quote)
        quote['ar'][0]['price'] = 19500
        replacement = self.data / 'replacement.json'
        replacement.write_text(json.dumps(quote))
        replacement.replace(self.manual)
        status, headers, replaced = self.request(headers={'If-Modified-Since':'Wed, 31 Dec 2099 23:59:59 GMT'})
        self.assertEqual(status,200)
        self.assertEqual(json.loads(replaced)['ar'][0]['price'],19500)
        self.assertEqual(headers['cache-control'],'no-store')

    def test_head_and_query_string_use_only_the_named_live_file(self):
        content = json.dumps({'ar':[],'us':[],'note':'Riñón'},ensure_ascii=False).encode('utf8')
        self.manual.write_bytes(content)
        status, headers, body = self.request('/data/manual-prices.json?path=../../secret.txt',method='HEAD')
        self.assertEqual(status,200)
        self.assertEqual(body,b'')
        self.assertEqual(int(headers['content-length']),len(content))
        self.assertEqual(headers['content-type'],'application/json; charset=utf-8')
        self.assertEqual(headers['x-content-type-options'],'nosniff')
        self.assertEqual(self.request('/data/manual-prices.json?revision=2')[2],content)

    def test_missing_file_is_empty_and_later_creation_is_visible_without_restart(self):
        self.manual.unlink()
        self.assertEqual(self.request()[2],EMPTY_MANUAL)
        self.manual.write_text('{"ar":[],"us":[],"revision":2}')
        self.assertEqual(json.loads(self.request()[2])['revision'],2)
        self.manual.unlink()
        self.assertEqual(self.request()[2],EMPTY_MANUAL)

    def test_symlink_replacement_including_broken_links_is_refused(self):
        secret = self.root / 'secret.json'
        secret.write_text('private contents')
        self.manual.unlink()
        self.manual.symlink_to(secret)
        status, _, body = self.request()
        self.assertEqual(status,403)
        self.assertNotIn(b'private contents',body)
        secret.unlink()
        self.assertEqual(self.request()[0],403)

    def test_nonregular_file_and_symlink_parent_are_refused(self):
        self.manual.unlink()
        self.manual.mkdir()
        self.assertEqual(self.request()[0],403)
        self.manual.rmdir()
        os.mkfifo(self.manual)
        self.assertEqual(self.request()[0],403)
        self.manual.unlink()
        self.data.rmdir()
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        (elsewhere / 'manual-prices.json').write_text('private contents')
        self.data.symlink_to(elsewhere,target_is_directory=True)
        self.assertEqual(self.request()[0],403)

    def test_oversize_file_rejects_and_valid_replacement_recovers(self):
        self.manual.write_bytes(b' ' * (MAX_MANUAL_BYTES+1))
        self.assertEqual(self.request()[0],413)
        self.manual.write_bytes(EMPTY_MANUAL)
        self.assertEqual(self.request()[0],200)

    def test_other_routes_serve_only_the_public_copy(self):
        (self.root / 'project' / 'secret.txt').write_text('private contents')
        self.assertEqual(self.request('/index.html')[2],b'Public atlas')
        for target in ['/secret.txt','/../project/secret.txt','/data/manual-prices.template.json','/%64ata/manual-prices.json']:
            status, _, body = self.request(target)
            self.assertEqual(status,404,target)
            self.assertNotIn(b'private contents',body)


if __name__ == '__main__':
    unittest.main()
