# -*- coding: utf-8 -*-

from .context import sdfonts_py

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNotNone(sdfonts_py.SDFonts())


if __name__ == '__main__':
    unittest.main()
