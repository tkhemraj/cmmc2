"""Test suite for CMMC 2.0 assessment tool."""

import unittest
from cmmc2.practices.catalog import (
    PRACTICES, LEVEL1_PRACTICES, LEVEL2_PRACTICES, get_practice,
    get_by_domain, get_by_level, DOMAINS,
)
from cmmc2.models.assessment import PracticeStatus, PracticeResult, CMMCAssessment
from cmmc2.scoring.scorer import CMMCScorer
from cmmc2.assessor import CMMCAssessor


class TestPracticeCatalog(unittest.TestCase):

    def test_level1_count(self):
        self.assertEqual(len(LEVEL1_PRACTICES), 17)

    def test_level2_count(self):
        self.assertEqual(len(LEVEL2_PRACTICES), 110)

    def test_get_practice(self):
        p = get_practice("3.1.1")
        self.assertIsNotNone(p)
        self.assertEqual(p.domain, "AC")
        self.assertEqual(p.level, 1)
        self.assertEqual(p.cmmc_id, "AC.L1-3.1.1")

    def test_all_practices_have_required_fields(self):
        for p in PRACTICES:
            self.assertTrue(p.nist_id)
            self.assertTrue(p.cmmc_id)
            self.assertTrue(p.domain)
            self.assertIn(p.level, (1, 2, 3))
            self.assertTrue(p.title)
            self.assertGreater(p.sprs_weight, 0)

    def test_domains_present(self):
        for domain in ["AC", "AT", "AU", "CM", "IA", "IR", "MA", "MP", "PE", "PS",
                       "RA", "CA", "SC", "SI"]:
            self.assertIn(domain, DOMAINS)

    def test_get_by_domain(self):
        ac_practices = get_by_domain("AC")
        self.assertGreater(len(ac_practices), 0)
        self.assertTrue(all(p.domain == "AC" for p in ac_practices))

    def test_sprs_max(self):
        from cmmc2.practices.catalog import MAX_SPRS_SCORE
        self.assertEqual(MAX_SPRS_SCORE, 110)


class TestAssessmentModels(unittest.TestCase):

    def _make_result(self, nist_id, status):
        p = get_practice(nist_id)
        return PracticeResult(
            nist_id=p.nist_id, cmmc_id=p.cmmc_id,
            domain=p.domain, level=p.level, status=status,
        )

    def test_practice_result_serialization(self):
        r = self._make_result("3.1.1", PracticeStatus.COMPLIANT)
        d = r.to_dict()
        self.assertEqual(d["status"], "Compliant")
        restored = PracticeResult.from_dict(d)
        self.assertEqual(restored.status, PracticeStatus.COMPLIANT)
        self.assertEqual(restored.nist_id, "3.1.1")

    def test_assessment_serialization(self):
        assessment = CMMCAssessment(customer="Test Corp", target_level=2)
        assessment.results["3.1.1"] = self._make_result("3.1.1", PracticeStatus.COMPLIANT)
        d = assessment.to_dict()
        restored = CMMCAssessment.from_dict(d)
        self.assertEqual(restored.customer, "Test Corp")
        self.assertEqual(len(restored.results), 1)
        self.assertEqual(restored.results["3.1.1"].status, PracticeStatus.COMPLIANT)

    def test_get_non_compliant(self):
        assessment = CMMCAssessment(customer="Test Corp", target_level=2)
        assessment.results["3.1.1"] = self._make_result("3.1.1", PracticeStatus.COMPLIANT)
        assessment.results["3.5.3"] = self._make_result("3.5.3", PracticeStatus.NON_COMPLIANT)
        self.assertEqual(len(assessment.get_non_compliant()), 1)

    def test_get_domain_results(self):
        assessment = CMMCAssessment(customer="Test Corp", target_level=2)
        assessment.results["3.1.1"] = self._make_result("3.1.1", PracticeStatus.COMPLIANT)
        assessment.results["3.5.3"] = self._make_result("3.5.3", PracticeStatus.NON_COMPLIANT)
        ac_results = assessment.get_domain_results("AC")
        self.assertEqual(len(ac_results), 1)
        self.assertEqual(ac_results[0].domain, "AC")


class TestScoring(unittest.TestCase):

    def _full_compliant_assessment(self) -> CMMCAssessment:
        """Assessment where every Level 2 practice is compliant."""
        assessment = CMMCAssessment(customer="Perfect Corp", target_level=2)
        for p in LEVEL2_PRACTICES:
            assessment.results[p.nist_id] = PracticeResult(
                nist_id=p.nist_id, cmmc_id=p.cmmc_id,
                domain=p.domain, level=p.level,
                status=PracticeStatus.COMPLIANT,
            )
        return assessment

    def test_perfect_sprs_score(self):
        assessment = self._full_compliant_assessment()
        score = CMMCScorer.calculate_sprs_score(assessment)
        self.assertEqual(score, 110)

    def test_sprs_deducts_for_non_compliant(self):
        assessment = self._full_compliant_assessment()
        # Mark MFA (3.5.3, weight=5) as non-compliant
        assessment.results["3.5.3"].status = PracticeStatus.NON_COMPLIANT
        score = CMMCScorer.calculate_sprs_score(assessment)
        self.assertEqual(score, 105)  # 110 - 5

    def test_sprs_deducts_for_not_assessed(self):
        assessment = self._full_compliant_assessment()
        assessment.results["3.1.1"].status = PracticeStatus.NOT_ASSESSED
        score = CMMCScorer.calculate_sprs_score(assessment)
        self.assertLess(score, 110)

    def test_level1_score(self):
        assessment = self._full_compliant_assessment()
        compliant, total, pct = CMMCScorer.calculate_level1_score(assessment)
        self.assertEqual(total, 17)
        self.assertEqual(compliant, 17)
        self.assertEqual(pct, 100.0)

    def test_achieved_level_2(self):
        assessment = self._full_compliant_assessment()
        self.assertEqual(CMMCScorer.determine_achieved_level(assessment), 2)

    def test_achieved_level_0_when_l1_fails(self):
        assessment = CMMCAssessment(customer="Bad Corp", target_level=2)
        # Only one practice, non-compliant
        p = get_practice("3.1.1")
        assessment.results["3.1.1"] = PracticeResult(
            nist_id=p.nist_id, cmmc_id=p.cmmc_id,
            domain=p.domain, level=p.level,
            status=PracticeStatus.NON_COMPLIANT,
        )
        self.assertEqual(CMMCScorer.determine_achieved_level(assessment), 0)

    def test_domain_scores(self):
        assessment = self._full_compliant_assessment()
        domain_scores = CMMCScorer.calculate_domain_scores(assessment)
        self.assertIn("AC", domain_scores)
        self.assertEqual(domain_scores["AC"]["percentage"], 100.0)

    def test_full_scorecard_keys(self):
        assessment = self._full_compliant_assessment()
        sc = CMMCScorer.full_scorecard(assessment)
        for key in ["sprs_score", "achieved_level", "target_level", "level1", "level2",
                    "domains", "non_compliant_count", "non_compliant_ids"]:
            self.assertIn(key, sc)


class TestAssessor(unittest.TestCase):

    def test_full_assessment_runs(self):
        assessor = CMMCAssessor("Integration Test Corp", target_level=2)
        assessment = assessor.assess()
        self.assertIsNotNone(assessment)
        self.assertEqual(assessment.customer, "Integration Test Corp")
        self.assertGreater(len(assessment.results), 0)

    def test_scorecard_after_assess(self):
        assessor = CMMCAssessor("Scorecard Corp", target_level=2)
        assessor.assess()
        sc = assessor.scorecard
        self.assertIsNotNone(sc)
        self.assertIn("sprs_score", sc)
        self.assertLessEqual(sc["sprs_score"], 110)

    def test_export_json(self):
        import tempfile, json, os
        assessor = CMMCAssessor("Export Test Corp", target_level=2)
        assessor.assess()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            success = assessor.export("json", path)
            self.assertTrue(success)
            with open(path) as f:
                data = json.load(f)
            self.assertIn("assessment", data)
            self.assertIn("scorecard", data)
        finally:
            os.unlink(path)

    def test_export_html(self):
        import tempfile, os
        assessor = CMMCAssessor("HTML Test Corp", target_level=2)
        assessor.assess()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            path = f.name
        try:
            success = assessor.export("html", path)
            self.assertTrue(success)
            self.assertGreater(os.path.getsize(path), 1000)
        finally:
            os.unlink(path)

    def test_export_poam(self):
        import tempfile, os
        assessor = CMMCAssessor("POAM Test Corp", target_level=2)
        assessor.assess()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            path = f.name
        try:
            success = assessor.export("poam", path)
            self.assertTrue(success)
            self.assertGreater(os.path.getsize(path), 500)
        finally:
            os.unlink(path)

    def test_export_before_assess_fails(self):
        assessor = CMMCAssessor("No Assess Corp", target_level=2)
        success = assessor.export("json", "/tmp/should_not_exist.json")
        self.assertFalse(success)

    def test_covers_all_110_practices(self):
        assessor = CMMCAssessor("Coverage Corp", target_level=2)
        assessment = assessor.assess()
        # Should have a result for every Level 2 practice
        assessed_ids = set(assessment.results.keys())
        l2_ids = {p.nist_id for p in LEVEL2_PRACTICES}
        missing = l2_ids - assessed_ids
        self.assertEqual(missing, set(), f"Missing practices: {missing}")


if __name__ == "__main__":
    unittest.main()
