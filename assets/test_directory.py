#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from version_directory import VersionDirectory

class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.source = {
            'url': '...',
            'version-prefix': 'bbb-',
            'prefix': 'aaa-'
        }
        self.dir = VersionDirectory(self.source, None)

    def test_init_with_version_prefix(self):
        self.assertEqual('bbb-', self.dir.version_prefix)

if __name__ == '__main__':
    unittest.main()
