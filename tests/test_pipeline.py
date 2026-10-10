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
if __name__=="__main__": unittest.main()
