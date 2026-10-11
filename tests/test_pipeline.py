import pathlib, tempfile, unittest, sys
import pandas as pd
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"code"))
from extract_ownership import run

class TestPipeline(unittest.TestCase):
    def test_historical_filter_and_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            pd.DataFrame([
             {"Institution":"Alpha","Year":1925,"Sentence_Cleaned":"University shall own all patents."},
             {"Institution":"Alpha","Year":1944,"Sentence_Cleaned":"University shall own patentable inventions."},
             {"Institution":"Beta","Year":2025,"Sentence_Cleaned":"Faculty retain ownership of scholarly works."},
             {"Institution":"Beta","Year":2025,"Sentence_Cleaned":"Nothing relevant."},
            ]).to_csv(root/"input.csv",index=False)
            counts,review=run(root/"input.csv",root/"out")
            self.assertEqual(len(counts),2)
            self.assertEqual(len(review),2)
            self.assertFalse((counts.Year==1925).any())

class TestFrozenResearchPackage(unittest.TestCase):
    root=pathlib.Path(__file__).resolve().parents[1]
    def test_source_checksums(self):
        import json,hashlib
        for r in json.loads((self.root/'data/source_manifest.json').read_text())['files']:
            p=self.root/'input'/r['local_name']
            self.assertTrue(p.exists(),'Run code/fetch_sources.py first')
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['sha256'])
    def test_population_denominators(self):
        import json
        a=json.loads((self.root/'results/corpus_audit.json').read_text())
        self.assertEqual((a['institutions'],a['observed_records'],a['included_rows'],a['panel_rows']),(150,480,87159,4277))
        self.assertEqual(a['observed_records']+a['carried_forward_rows'],a['panel_rows'])
        self.assertEqual(a['candidate_sentences'],2779)
        self.assertEqual(a['candidate_records'],449)
        self.assertEqual(a['excluded_rows'],1)
    def test_unique_row_ids_despite_sentence_collisions(self):
        x=pd.read_csv(self.root/'results/sentence_index.csv')
        self.assertTrue(x.sentence_id.is_unique)
        self.assertEqual(int(x.sentence_key_collision.sum()),3662)
        self.assertTrue(x.groupby('sentence_id').text_sha256.nunique().eq(1).all())
    def test_all_category_transitions_reconcile(self):
        x=pd.read_csv(self.root/'results/lexical_transition_matrix.csv')
        self.assertEqual(len(x),9)
        self.assertTrue(x.iloc[:,1:].sum(axis=1).eq(330).all())
        p=pd.read_csv(self.root/'results/category_mention_pairs.csv')
        self.assertTrue((p.after-p.before).equals(p.change))
        self.assertFalse(p.duplicated(['Institution','from_year','to_year','category']).any())
    def test_no_interpolated_vintages(self):
        v=pd.read_csv(self.root/'results/frozen_observed_population.csv')
        keys=set(map(tuple,v[['Institution','Year']].values))
        p=pd.read_csv(self.root/'results/observed_vintage_pairs.csv')
        self.assertEqual(len(p),330)
        self.assertEqual(p.Institution.nunique(),129)
        for r in p.itertuples():
            self.assertIn((r.Institution,r.from_year),keys)
            self.assertIn((r.Institution,r.to_year),keys)
            self.assertGreater(r.to_year,r.from_year)
    def test_sampling_weights_and_negative_cases(self):
        s=pd.read_csv(self.root/'results/validation_sample_manifest.csv')
        self.assertEqual(len(s),178)
        self.assertTrue(s.sentence_id.is_unique)
        self.assertEqual(set(s.candidate),{True,False})
        self.assertTrue(((s.stratum_sample/s.stratum_population)-s.inclusion_probability).abs().lt(1e-12).all())
    def test_validation_not_fabricated(self):
        import json
        a=json.loads((self.root/'results/validation_status.json').read_text())
        self.assertEqual(a['independent_human_annotators'],0)
        for k in ['precision','recall','agreement']:self.assertIsNone(a[k])
        e=pd.read_csv(self.root/'results/illustrative_legal_evidence.csv')
        self.assertFalse(e.independent_human_validation.any())
        self.assertTrue(e.enforceability.eq('not_adjudicated').all())
        template=pd.read_csv(self.root/'results/validation_annotation_template.csv')
        self.assertTrue(template.annotator_id.isna().all())
    def test_actual_missed_provisions_remain_visible(self):
        e=pd.read_csv(self.root/'results/illustrative_legal_evidence.csv').set_index('sentence_id')
        for sid in ['p1r002641','p1r010577','p1r070766']:
            self.assertFalse(e.loc[sid,'original_screen_candidate'])
            self.assertTrue(e.loc[sid,'expanded_review_candidate'])
        # These are retrieval checks, not legal accuracy tests.
    def test_context_not_promoted_to_exact_vintage(self):
        e=pd.read_csv(self.root/'results/illustrative_legal_evidence.csv')
        self.assertTrue(e[e.source_id.eq('wfu1999')].context_status.eq('later_reprint_not_exact_vintage').all())
        self.assertTrue(e[e.source_id.eq('palmer1962')].context_status.eq('historical_corroboration_not_exact_vintage').all())
    def test_bibliography_corrections_and_resolution(self):
        import json
        r={r['key']:r for r in json.loads((self.root/'references/accepted_records.json').read_text())}
        self.assertGreaterEqual(len(r),40)
        self.assertEqual(r['dasgupta1994']['authors'][0]['family'],'Dasgupta')
        self.assertEqual(r['nrc2011']['year'],2011)
        self.assertEqual(r['rai2003']['year'],2003)
        self.assertEqual(r['rai2003']['doi'],'')
        a=json.loads((self.root/'results/manuscript_audit.json').read_text())
        self.assertEqual(a['unresolved_citations'],[])
        self.assertEqual(a['uncited_entries'],[])
        self.assertLessEqual(a['abstract_words'],150)
    def test_overleaf_mirror(self):
        from sync_overleaf import sync
        sync(check=True)

if __name__=="__main__": unittest.main()
