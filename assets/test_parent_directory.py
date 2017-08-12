#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import unittest
import sys
from httmock import urlmatch, HTTMock
from semantic_version import Version
from parent_directory import ParentDirectory

class TestParentDirectory(unittest.TestCase):
    def setUp(self):
        sys.stderr = io.StringIO()
        self.maxDiff = None
        self.versionify = lambda v: Version(v, partial=True)
        self.hadoop_dir = ParentDirectory({
            'url': 'http://www-us.apache.org/dist/hadoop/core/?F=2',
            'prefix': 'hadoop-'
        })
        self.hbase_dir = ParentDirectory({
            'url': 'http://www-us.apache.org/dist/hbase/?F=2'
        })

    @urlmatch(netloc=r'hadoop/core/\?F=2$')
    def hadoop_mock(url, request):
        projroot = os.path.realpath(__file__)
        fix = os.path.join(projroot, 'fixtures', 'hadoop-versions.htm')
        return open(fix).read()

    @urlmatch(netloc=r'hbase/\?F=2$')
    def hbase_mock(url, request):
        projroot = os.path.realpath(__file__)
        fix = os.path.join(projroot, 'fixtures', 'hbase-versions.htm')
        return open(fix).read()

    def test_fetch_all_versions_apache(self):
        expected = list(map(self.versionify, [
            '1.2.1', '2.6.1', '2.6.2', '2.6.3', '2.6.4', '2.6.5', '2.7.0',
            '2.7.1', '2.7.2', '2.7.3', '2.7.4', '2.8.0', '2.8.1',
            '3.0.0-alpha1', '3.0.0-alpha2', '3.0.0-alpha3', '3.0.0-alpha4'
        ]))
        with HTTMock(self.hadoop_mock):
            self.hadoop_dir.fetch()
            self.assertCountEqual(expected, self.hadoop_dir.versions)

    def test_fetch_all_versions_apache_no_prefix(self):
        expected = list(map(self.versionify, [
            '1.1.11', '1.2.6', '1.3.1', '2.0.0-alpha-1'
        ]))
        with HTTMock(self.hbase_mock):
            self.hbase_dir.fetch()
            self.assertCountEqual(expected, self.hbase_dir.versions)

    def test_fetch_new_versions_apache(self):
        expected = list(map(self.versionify, [
            '2.7.2', '2.7.3', '2.7.4', '2.8.0', '2.8.1', '3.0.0-alpha1',
            '3.0.0-alpha2', '3.0.0-alpha3', '3.0.0-alpha4'
        ]))
        with HTTMock(self.hadoop_mock):
            self.hadoop_dir.fetch('2.7.1')
            self.assertCountEqual(expected, self.hadoop_dir.versions)

    def test_to_json(self):
        expected = list(map(lambda v: {'version': v}, [
            '3.0.0-alpha1', '3.0.0-alpha2', '3.0.0-alpha3', '3.0.0-alpha4'
        ]))
        with HTTMock(self.hadoop_mock):
            self.hadoop_dir.fetch('2.8.1')
        self.assertCountEqual(expected, self.hadoop_dir.to_json())

if __name__ == '__main__':
    unittest.main()
