"""Bounded current-brand checks; compatibility tokens are not new identities."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
OLD='Mind'+'OS'
COMPAT_DOCS={'docs/MIGRATION.md',f'docs/WHY_{OLD.upper()}.md'}
TOKENS={
    f'docs/WHY_{OLD.upper()}.md':'PUBLIC_COMPAT',
    f'core/{OLD}.md':'PUBLIC_COMPAT',
    f'GLOBAL/{OLD}.md':'HISTORICAL_PROVENANCE',
    f'{OLD.lower()}-public-assets@1':'SCHEMA_OR_MACHINE_IDENTIFIER',
    f'{OLD.lower()}_inbox_router':'SCHEMA_OR_MACHINE_IDENTIFIER',
    f'{OLD.lower()}_local_probe':'SCHEMA_OR_MACHINE_IDENTIFIER',
    f'{OLD.upper()}-':'SCHEMA_OR_MACHINE_IDENTIFIER',
    f'old `{OLD.lower()}` Skills':'PUBLIC_COMPAT',
    f'Original compact {OLD} mark':'HISTORICAL_PROVENANCE',
}

def classify(root):
    records=[]
    for path in sorted(Path(root).rglob('*')):
        if not path.is_file() or '.git' in path.parts or path.suffix=='.png':continue
        rel=path.relative_to(root).as_posix()
        text=path.read_text(encoding='utf-8-sig')
        for number,line in enumerate(text.splitlines(),1):
            for match in re.finditer(OLD,line,re.I):
                category='UNKNOWN'
                if rel in COMPAT_DOCS:category='PUBLIC_COMPAT'
                else:
                    for token,kind in TOKENS.items():
                        for found in re.finditer(re.escape(token),line):
                            if found.start()<=match.start()<found.end():category=kind
                records.append({'path':rel,'line':number,'column':match.start()+1,'category':category,'text':line})
    return records

class RebrandTests(unittest.TestCase):
    def test_no_unclassified_old_brand(self):
        self.assertEqual([], [r for r in classify(ROOT) if r['category']=='UNKNOWN'])

    def test_canonical_brand_and_thin_compatibility(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertIn('# FarRefrain',readme)
        self.assertIn('A project continuity substrate for AI-native work.',readme)
        self.assertEqual(1,readme.count('The singer changes. The refrain continues.'))
        old=ROOT/'docs'/f'WHY_{OLD.upper()}.md'
        self.assertLess(len(old.read_bytes()),400)
        self.assertIn('WHY_FARREFRAIN.md',old.read_text(encoding='utf-8'))
        self.assertTrue((ROOT/'core/MEMORY_CONTRACT.md').is_file())
        self.assertFalse((ROOT/'core/FarRefrain.md').exists())
        self.assertIn('\nname: default\n',(ROOT/'workflows/default/SKILL.md').read_text(encoding='utf-8'))
        manifest=json.loads((ROOT/'docs/asset-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(OLD.lower()+'-public-assets@1',manifest['schema'])

    def test_old_visual_names_are_retired(self):
        assets={p.name for p in (ROOT/'assets').iterdir()}
        self.assertEqual({'farrefrain-hero.svg','farrefrain-mark.svg','farrefrain-workflow.svg',
                          'farrefrain-social-preview.svg','farrefrain-social-preview.png'},assets)

if __name__=='__main__':unittest.main()
