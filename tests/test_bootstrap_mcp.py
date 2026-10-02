import argparse
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/bootstrap_mcp.py'
spec=importlib.util.spec_from_file_location('bootstrap_mcp_test',SCRIPT)
bootstrap=importlib.util.module_from_spec(spec);spec.loader.exec_module(bootstrap)


class BootstrapTests(unittest.TestCase):
    def test_durable_platform_paths_and_relative_env_fallback(self):
        home=PurePosixPath('/users/example')
        self.assertEqual(bootstrap.default_data_root('darwin',{},home),home/'Library/Application Support/codex-setup')
        self.assertEqual(bootstrap.default_data_root('linux',{'XDG_DATA_HOME':'relative'},home),home/'.local/share/codex-setup')
        self.assertEqual(bootstrap.default_data_root('linux',{'XDG_DATA_HOME':'/data'},home),PurePosixPath('/data/codex-setup'))
    def test_migration_preserves_unrelated_and_nested_credentials(self):
        original='model="existing"\n# BEGIN codex-setup Jev MCP\n[mcp_servers.jev]\ncommand="old"\nargs=["-B","/skills/jev-evaluation/scripts/mcp_server.py"]\nenv_vars=["TYPESAFE_API_KEY"]\n[mcp_servers.jev.env]\nPRIVATE="keep"\n# END codex-setup Jev MCP\n[mcp_servers.node_repl]\ncommand="node_repl.exe"\n'
        new=bootstrap.registration(original,'jev',{'command':'new','args':['-I','-m','codex_jev_mcp.mcp_server'],'env_vars':['TYPESAFE_API_KEY','JEV_TELEMETRY']},existing=True)
        import tomllib
        before,after=tomllib.loads(original),tomllib.loads(new)
        self.assertEqual(after['mcp_servers']['jev']['env'],before['mcp_servers']['jev']['env'])
        self.assertEqual(after['mcp_servers']['node_repl'],before['mcp_servers']['node_repl'])
        self.assertEqual(after['model'],before['model'])
    def test_unknown_registration_not_owned(self):
        spec={'kind':'python','name':'jev','module':'codex_jev_mcp.mcp_server'}
        self.assertFalse(bootstrap.owned({'command':'python','args':['unknown.py']},spec,''))
    def test_skill_sync_backup_outside_mirror_and_repeat_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';target=root/'skills/jev-evaluation'
            source.mkdir();(source/'SKILL.md').write_text('new')
            target.mkdir(parents=True);(target/'SKILL.md').write_text('old')
            first=bootstrap.sync_skill(source,target)
            self.assertEqual(first['changed_files'],1);self.assertEqual(Path(first['backups'][0]).read_text(),'old')
            self.assertFalse(Path(first['backups'][0]).is_relative_to(target))
            self.assertEqual(bootstrap.sync_skill(source,target)['changed_files'],0)
            (target/'unknown.txt').write_text('private')
            with self.assertRaises(ValueError):bootstrap.sync_skill(source,target)
    def test_preview_no_writes_new_roots_pending_and_existing_permission_retained(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);config=root/'config.toml'
            config.write_text('[mcp_servers.local_documents]\ncommand='+json.dumps(str(root/'runtime/python'))+'\nargs=["-m","mcp_servers.local_documents.document_server","--read-root","/allowed","--write-root","/allowed"]\n[mcp_servers.docs]\nurl="https://developers.openai.com/mcp"\n')
            before=config.read_bytes()
            args=argparse.Namespace(config=config,bundle=root/'missing',runtime_root=root/'runtime',read_root=[],context7=False,cert=None)
            with patch.dict(bootstrap.os.environ,{'CODEX_HOME':str(root)}),patch.object(bootstrap,'runtime_info',return_value=None):
                report,context=bootstrap.plan(args)
            by_name={item['name']:item for item in report['servers']}
            self.assertEqual(by_name['workspace_inspection']['status'],'pending_roots')
            self.assertEqual(by_name['openaiDeveloperDocs']['status'],'reuse_provider')
            self.assertIn('--write-root',by_name['local_documents']['registration']['args'])
            self.assertEqual(config.read_bytes(),before);self.assertFalse((root/'mcp-bootstrap.json').exists())
            self.assertFalse((root/'runtime').exists())
    def test_atomic_concurrent_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'config';path.write_bytes(b'changed')
            with self.assertRaises(ValueError):bootstrap.atomic(path,b'new',b'old')
            self.assertEqual(path.read_bytes(),b'changed')
    def test_read_root_is_not_forwarded_to_new_jev(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            args=argparse.Namespace(config=root/'config.toml',bundle=root/'missing',runtime_root=root/'runtime',read_root=[root],context7=False,cert=None)
            with patch.dict(bootstrap.os.environ,{'CODEX_HOME':str(root)}):
                report,_=bootstrap.plan(args)
            jev=next(item for item in report['servers'] if item['name']=='jev')
            self.assertNotIn('--read-root',jev['registration']['args'])
    def test_multiline_verifier_json_and_repeated_registration(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);runtime=root/'runtime';runtime.mkdir()
            python=runtime/'python';python.touch()
            (runtime/'codex-mcp-wheels.json').write_text(json.dumps({'sample':'hash'}))
            item={'name':'sample','status':'new','existing':False,'python':str(python),'runtime':str(runtime),'runtime_info':{'packages':{'sample':'1'}},'wheels':[{'name':'sample','sha256':'hash','version':'1'}],'spec':{'kind':'python','packages':{'sample':'1'},'verify_module':'sample.verify'},'registration':{'command':str(python),'args':['-m','sample.server']}}
            config=root/'config.toml';context=(config,None,'',root/'state.json',{'servers':{}},root)
            def output(command,**kwargs):return json.dumps({'status':'passed','tools':['a']},indent=2) if 'sample.verify' in command else ''
            with patch.object(bootstrap,'run',side_effect=output):
                result=bootstrap.apply({'servers':[item],'bundle':str(root),'sync_jev_skill':False},context)
            self.assertEqual(result['servers'][0]['verification']['status'],'passed')
            self.assertEqual(result['servers'][0]['status'],'ready')

if __name__=='__main__':unittest.main()
