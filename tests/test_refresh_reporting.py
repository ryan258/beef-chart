"""Expected provider failures are readable while unexpected bugs remain visible."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('retail_reporting', ROOT / 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)


class RefreshReporting(unittest.TestCase):
    def test_native_prices_and_failed_requests_are_distinguished(self):
        attempted = '2026-10-15T18:15:23Z'
        data = {
            'fx': {'period':'2026-08'},
            'ar_sources': {'IPCVA': {'lomo':{'period':'2026-09'}}},
            'carrefour_originals': {'lomo':{'period':'2026-10-07'}},
            'source_status': {
                'IPCVA': {'status':'partial','attempted_at':attempted,
                          'coverage':{'lomo':'observed'},
                          'note':'Matching monthly FX unavailable for 2026-09; native ARS/kg saved'},
                'FX monthly': {'status':'ok','attempted_at':attempted},
                'Carrefour AR': {'status':'error','attempted_at':attempted,
                                 'coverage':{'lomo':'error'},'note':'HTTP 403 Forbidden'},
                'USDA ad survey': {'status':'error','attempted_at':attempted,'error_type':'TimeoutError'},
                'Old source': {'status':'ok','attempted_at':'2026-10-14T00:00:00Z'},
            },
        }
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            retail.print_refresh_summary(data,['IPCVA','Carrefour','USDA'],attempted)
        text = output.getvalue()
        self.assertIn('IPCVA: partial; 1/1 observations accepted; stored price month 2026-09',text)
        self.assertIn('Matching monthly FX unavailable for 2026-09; native ARS/kg saved',text)
        self.assertIn('FX monthly: ok; stored FX month 2026-08',text)
        self.assertIn('Carrefour AR: error; 0/1 observations accepted; 1 failed; HTTP 403 Forbidden',text)
        self.assertIn('USDA ad survey: error; TimeoutError',text)
        self.assertIn('Original Carrefour archive: 1 observations preserved',text)
        self.assertNotIn('Old source',text)

    def test_expected_partial_refresh_exits_nonzero_without_traceback(self):
        code = '''
import importlib.util
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('retail', 'scrape-retail.py')
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)
with patch.object(retail, 'main', side_effect=retail.PartialRefreshError(['IPCVA','Carrefour','USDA'])):
    retail.cli()
'''
        result = subprocess.run([sys.executable,'-c',code],cwd=ROOT,capture_output=True,text=True,timeout=5)
        self.assertEqual(result.returncode,1)
        self.assertIn('Partial refresh: 3 source issues; see results above.',result.stderr)
        self.assertNotIn('Traceback',result.stderr)

    def test_unexpected_programming_errors_are_not_suppressed(self):
        with patch.object(retail,'main',side_effect=RuntimeError('unexpected bug')):
            with self.assertRaisesRegex(RuntimeError,'unexpected bug'):
                retail.cli()


if __name__ == '__main__':
    unittest.main()
