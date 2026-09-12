import importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('projection',Path(__file__).resolve().parents[1]/'tools/context_projection.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'source.md').write_text('Decision evidence, including prior failure.',encoding='utf-8')
    def tearDown(self):self.tmp.cleanup()
    def make(self,name,status='ADOPTED',kind='FACT',scope='global',role='current',primary=False):
        meta={'truth_status':status,'knowledge_type':kind,'scope':[scope],'primary':primary,'evidence':['source.md']}
        (self.root/name).write_text('---\n'+json.dumps(meta)+'\n---\nScoped record.',encoding='utf-8')
        return p.record(self.root,name,role)
    def test_projection_and_gotcha_scope(self):
        records=[self.make('primary.md',primary=True),self.make('idea.md','PROPOSED',role='planning'),self.make('build.md',kind='GOTCHA',scope='build'),self.make('audio.md',kind='FAILURE',scope='audio'),self.make('conflict.md','CONTESTED',scope='build')]
        self.assertEqual(['primary.md'],p.choose(records,0))
        self.assertEqual(['primary.md'],p.choose(records,1))
        self.assertEqual(['primary.md','build.md','conflict.md'],p.choose(records,2,scopes=['build']))
        self.assertNotIn('idea.md',p.choose(records,2,scopes=['build']))
    def test_promotion_and_history(self):
        r=self.make('candidate.md','PROPOSED')
        for kwargs in [{},{'automatic':False},{'authorized':True,'automatic':False}]:
            with self.assertRaises(ValueError):p.promotion(self.root,'candidate.md',**kwargs)
        self.assertTrue(p.promotion(self.root,'candidate.md',authorized=True,automatic=False,unresolved_conflict=False)['permitted'])
        self.assertEqual('PROPOSED',p.record(self.root,'candidate.md','current')['truth_status'])
        old=self.make('old.md','SUPERSEDED',role='history');current=self.make('now.md',primary=True)
        self.assertNotIn('old.md',p.choose([current,old],1))
        self.assertIn('old.md',p.choose([current,old],3,evidence_paths=['old.md']))
    def test_missing_evidence_and_invalid_role(self):
        with self.assertRaises(ValueError):self.make('wrong.md',role='planning')
        self.make('candidate.md','PROPOSED')
        (self.root/'source.md').unlink()
        with self.assertRaises(ValueError):p.record(self.root,'candidate.md','current')
    def test_legacy_budget_and_missing_primary(self):
        (self.root/'legacy.md').write_text('Adopted plain file; existing layout.',encoding='utf-8')
        r=p.record(self.root,'legacy.md','current')
        self.assertEqual('ADOPTED',r['truth_status'])
        with self.assertRaises(ValueError):p.choose([r],0)
        paths=p.choose([r],0,primary_paths=['legacy.md'])
        self.assertEqual(paths,['legacy.md'])
        a=p.account(self.root,paths,0,target=(1,2))
        self.assertTrue(a['over_budget']);self.assertEqual(a,p.account(self.root,paths,0,target=(1,2)))
    def test_invalid_explicit_not_legacy_and_escape(self):
        (self.root/'broken.md').write_text('---\n{}\n---\nnot adopted',encoding='utf-8')
        with self.assertRaises(ValueError):p.record(self.root,'broken.md','current')
        with self.assertRaises(ValueError):p.local(self.root,'../outside.md')
if __name__=='__main__':unittest.main()
