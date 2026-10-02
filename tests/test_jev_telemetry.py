from contextlib import closing
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

SCRIPTS=Path(__file__).resolve().parents[1]/'skills/jev-evaluation/scripts'
sys.path.insert(0,str(SCRIPTS))
import jev
import jev_telemetry as telemetry


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.db=self.root/'events.sqlite'
        self.env=patch.dict(os.environ,{'CODEX_HOME':str(self.root),'JEV_TELEMETRY':'1'})
        self.env.start()
    def tearDown(self):
        self.env.stop();self.temp.cleanup()
    def enable(self):
        folder=self.root/'monitoring';folder.mkdir()
        (folder/'jev-monitor.json').write_text(json.dumps({'version':1,'enabled':True,'database':str(self.db)}))
    def rows(self):
        with closing(sqlite3.connect(self.db)) as db:
            return [json.loads(raw) for raw, in db.execute('SELECT metadata FROM jev_events')]
    def input(self):
        return {'state':'PRIVATE_QUERY', 'questions':{'private-id':{'type':'noul','instructions':'PRIVATE_RUBRIC'}}}
    def test_disabled_creates_no_file(self):
        jev.evaluate_data(self.input(),dry_run=True)
        self.assertFalse(self.db.exists());self.assertFalse((self.root/'monitoring').exists())
    def test_skipped_dryrun_and_validation_failure_are_local_safe_metadata(self):
        self.enable()
        with jev.source('cli'):
            jev.evaluate_data(self.input(),dry_run=True)
            jev.evaluate_data({'query':'PRIVATE_QUERY','candidates':[{'id':'PRIVATE_ID','required':True}]},rank=True)
            with self.assertRaises(jev.Problem): jev.evaluate_data({'state':'PRIVATE_QUERY','questions':{}})
        rows=self.rows()
        self.assertEqual([e['status'] for e in rows],['dry_run','skipped','fallback'])
        self.assertTrue(all(e['source']=='cli' for e in rows))
        self.assertTrue(all(e['input_tokens'] is None and not e['attempts'] for e in rows))
        self.assertNotIn('PRIVATE',json.dumps(rows))
    def test_retry_is_one_logical_call_two_attempts_with_known_usage(self):
        self.enable()
        raw={'model':'jev-1.13','answers':{'private-id':{'type':'noul','noul':.9}},'usage':{'input_tokens':7,'output_tokens':2}}
        response=MagicMock();response.read.return_value=json.dumps(raw).encode();response.status=200
        opener=MagicMock();opener.open.side_effect=[HTTPError('https://api.typesafe.ai/v1/systemone',503,'PRIVATE_ERROR',{},None),MagicMock(__enter__=MagicMock(return_value=response),__exit__=MagicMock(return_value=False))]
        with patch.object(jev,'load_key',return_value=('PRIVATE_KEY','environment')),patch.object(jev.request,'build_opener',return_value=opener),patch.object(jev.time,'sleep'):
            result,code=jev.evaluate_data(self.input())
        self.assertEqual(code,0);self.assertEqual(result['status'],'ok')
        rows=self.rows();self.assertEqual(len(rows),1)
        row=rows[0];self.assertEqual(row['input_tokens'],7);self.assertEqual(row['output_tokens'],2)
        self.assertEqual(len(row['attempts']),2);self.assertIsNone(row['attempts'][0]['response_bytes'])
        self.assertEqual(row['attempts'][0]['http_status'],503)
        self.assertNotIn('PRIVATE',json.dumps(row))
    def test_invalid_response_usage_still_known_without_storing_answers(self):
        self.enable()
        response=MagicMock();response.read.return_value=json.dumps({'model':'jev-1.13','answers':'PRIVATE_ANSWER','usage':{'input_tokens':10,'output_tokens':1}}).encode()
        opener=MagicMock();opener.open.return_value.__enter__.return_value=response
        with patch.object(jev,'load_key',return_value=('private','environment')),patch.object(jev.request,'build_opener',return_value=opener):
            result,_=jev.evaluate_data(self.input())
        self.assertEqual(result['status'],'fallback');self.assertEqual(self.rows()[0]['input_tokens'],10)
        self.assertNotIn('PRIVATE',json.dumps(self.rows()))
    def test_sqlite_failure_does_not_change_client_result(self):
        self.enable()
        with patch.object(telemetry.sqlite3,'connect',side_effect=OSError('PRIVATE_PATH')):
            result,code=jev.evaluate_data(self.input(),dry_run=True)
        self.assertEqual(code,0);self.assertEqual(result['status'],'dry_run');self.assertFalse(self.db.exists())
    def test_invalid_config_and_disable_fail_open(self):
        self.enable();(self.root/'monitoring/jev-monitor.json').write_text('invalid')
        self.assertEqual(jev.evaluate_data(self.input(),dry_run=True)[1],0)
        self.assertFalse(self.db.exists())

if __name__=='__main__':unittest.main()
