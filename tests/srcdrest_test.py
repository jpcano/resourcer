# -*- coding: utf-8 -*-

import unittest
import context

from srcdrest import SrcdRest

class TestSuite(unittest.TestCase):
    """TestSuite"""

    def test_linkedin(self):
        rest = SrcdRest()
        self.assertEqual(rest.getLinkedin('jcanovel@gmail.com'),
                         'http://es.linkedin.com/in/jesuscano1')

    def test_github(self):
        rest = SrcdRest()
        self.assertEqual(rest.getGithub('jcanovel@gmail.com'),
                         'http://github.com/jpcano')

    def test_linkedinNone(self):
        rest = SrcdRest()
        self.assertEqual(rest.getLinkedin('me@ruben.io'),
                         '')
        self.assertIsNone(rest.person['Profiles'])

    def test_githubGuestProfileNone(self):
        rest = SrcdRest()
        self.assertEqual(rest.getGithub('me@ruben.io'),
                         'https://github.com/Istar-Eldritch')
        self.assertIsNone(rest.person['Profiles'])

    def test_githubGuestGithubNone(self):
        rest = SrcdRest()
        self.assertEqual(rest.getGithub('inelegr88@gmail.com'),
                         'https://github.com/Geekfish')
        self.assertNotIn('github', rest.person['Profiles'])

    def test_linkedinEmpty(self):
        rest = SrcdRest()
        with self.assertRaises(ValueError) as cm:
            rest.getLinkedin('')

    def test_githubEmpty(self):
        rest = SrcdRest()
        with self.assertRaises(ValueError) as cm:
            rest.getGithub('')

    def test_linkedinNoExist(self):
        rest = SrcdRest()
        with self.assertRaises(ValueError) as cm:
            rest.getLinkedin('asdf1234@sourced.tech')
        
    def test_githubinNoExist(self):
        rest = SrcdRest()
        with self.assertRaises(ValueError) as cm:
            rest.getGithub('asdf1234@sourced.tech')

            
if __name__ == '__main__':
    unittest.main()
