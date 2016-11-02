# -*- coding: utf-8 -*-

import unittest
import context

from srcdplayground import SrcdPlayground

class TestSuite(unittest.TestCase):
    """TestSuite"""

    def test_getCountries(self):
        bq = SrcdPlayground()
        query = bq.getCountries()
        self.assertGreater(len(query), 0)  

    def test_getEcosystems(self):
        bq = SrcdPlayground()
        query = bq.getEcosystems()
        self.assertGreater(len(query), 0)  

    def test_getLanguages(self):
        bq = SrcdPlayground()
        query = bq.getLanguages()
        self.assertGreater(len(query), 0)
        
    def test_zero_results(self):
        bq = SrcdPlayground()
        langs = [['Copronti', True]]
        ecos = ['Yumiguay']
        countries = ['Somoscaia']
        report = False
        ANDlangs = True
        ANDecos = True
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertEqual(len(query), 0)

    def test_emptyParameters(self):
        bq = SrcdPlayground()
        langs = []
        ecos = []
        countries = []
        report = False
        ANDlangs = True
        ANDecos = True
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query), 0)  

    def test_some_results(self):
        bq = SrcdPlayground()
        langs = [['Java', False]]
        ecos = []
        countries = []
        report = False
        ANDlangs = True
        ANDecos = True
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query), 0)

    def test_reports(self):
        bq = SrcdPlayground()
        langs = [['Java', False]]
        ecos = []
        countries = []
        report = False
        ANDlangs = True
        ANDecos = True
        query1 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        report = True
        query2 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query1), len(query2))

    def test_variousLangs(self):
        bq = SrcdPlayground()
        langs = [['Python', False], ['Go', False]]
        ecos = []
        countries = []
        report = False
        ANDlangs = True
        ANDecos = True
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query), 0)

    def test_variousEcos(self):
        bq = SrcdPlayground()
        langs = []
        ecos = ['angular-js', 'react-js']
        countries = []
        report = False
        ANDlangs = True
        ANDecos = True
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query), 0)  

    def test_variousCountries(self):
        bq = SrcdPlayground()
        langs = []
        ecos = []
        countries = ['Spain', 'France']
        report = False
        ANDlangs = True
        ANDecos = True
        self.caca = 3
        query = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query), 0)

    def test_langORs(self):
        bq = SrcdPlayground()
        langs = [['Python', False], ['Go', False]]
        ecos = []
        countries = []
        report = False
        ANDlangs = False
        ANDecos = False
        query1 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        ANDlangs = True
        query2 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query1), len(query2))

    def test_ecoORs(self):
        bq = SrcdPlayground()
        langs = []
        ecos = ['flask', 'django']
        countries = []
        report = False
        ANDlangs = False
        ANDecos = False
        query1 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        ANDecos = True
        query2 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query1), len(query2))

    def test_countriesORs(self):
        bq = SrcdPlayground()
        langs = []
        ecos = []
        countries = ['Spain']
        report = False
        ANDlangs = False
        ANDecos = False
        query1 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        countries = ['Spain', 'Chile']
        query2 = bq.getQuery(langs, ecos, countries, report, ANDlangs, ANDecos)
        self.assertGreater(len(query2), len(query1))
        
    # def test_thoughts(self):
    #     # sample.hmm()
    #     self.assertEqual(33,3)
        
if __name__ == '__main__':
    unittest.main()
