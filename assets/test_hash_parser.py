#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
from hash_parser import HashParser

class TestMdsParser(unittest.TestCase):

    def __get_content(self, filename):
        projroot = os.path.dirname(__file__)
        fix = os.path.join(projroot, 'fixtures', filename)
        fh = open(fix)
        content =  fh.read()
        fh.close()
        return content

    def test_mds_format(self):
        self.p = HashParser('mds')
        content = self.__get_content('hadoop-2.7.3.tar.gz.mds')
        hashes = self.p.parse(content)
        self.assertEqual('b84b898934269c68753e4e036d21395e5a4ab5b1',
                self.p.get('hadoop-2.7.3.tar.gz', 'sha1'))
        self.assertEqual('3455bb57e4b4906bbea67b58cca78fa8',
                self.p.get('hadoop-2.7.3.tar.gz', 'md5'))
        self.assertEqual('52452d2f7d0b308f8bb53addb81d98d6d71f3a7cf5a0c5d8311c17dd902e052c3f4add3fee3c5ea2e6c749d3476e452fed50818d11001d87cfec039d9a8bade5',
                self.p.get('hadoop-2.7.3.tar.gz', 'sha512'))

    def test_sha1_format(self):
        self.p = HashParser('sha1')
        content = self.__get_content('zookeeper-3.4.9.tar.gz.sha1')
        hashes = self.p.parse(content)
        self.assertEqual('0285717bf5ea87a7a36936bf37851d214a32bb99',
                self.p.get('zookeeper-3.4.9.tar.gz', 'sha1'))

    def test_md5_format(self):
        self.p = HashParser('md5')
        content = self.__get_content('pig-0.17.0.tar.gz.md5')
        hashes = self.p.parse(content)
        self.assertEqual('da76998409fe88717b970b45678e00d4',
                self.p.get('pig-0.17.0.tar.gz', 'md5'))

if __name__ == '__main__':
    unittest.main()
