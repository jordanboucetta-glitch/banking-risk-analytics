import unittest
from pipeline import generate_loans, summary

class RiskTests(unittest.TestCase):
    def setUp(self):
        self.df = generate_loans(300, 42)

    def test_reproducibility(self):
        self.assertTrue(self.df.equals(generate_loans(300, 42)))

    def test_no_missing_and_unique_ids(self):
        self.assertFalse(self.df.isna().any().any())
        self.assertTrue(self.df.loan_id.is_unique)

    def test_valid_ranges(self):
        self.assertTrue(self.df.dti.between(0, 1).all())
        self.assertTrue((self.df.exposure_eur > 0).all())
        self.assertTrue(self.df.default_90d.isin([0, 1]).all())

    def test_aggregates(self):
        result = summary(self.df)
        self.assertEqual(int(result.loans.sum()), 300)
        self.assertEqual(int(result.exposure_eur.sum()), int(self.df.exposure_eur.sum()))

if __name__ == "__main__":
    unittest.main()
