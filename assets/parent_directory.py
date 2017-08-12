#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import htmllistparse
import json
from semantic_version import Version

from directory import Directory

class ParentDirectory(Directory):
    def __init__(self, source):
        super(ParentDirectory, self).__init__(source)
        if 'version-prefix' in source:
            self.version_prefix = source['version-prefix']
        elif 'prefix' in source:
            self.version_prefix = source['prefix']
        else:
            self.version_prefix = None
        if 'version-suffix' in source:
            self.version_suffix = source['version-suffix']
        elif 'suffix' in source:
            self.version_suffix = source['prefix']
        else:
            self.version_suffix = None
        self.versions = set()

    def __parse_entry(self, entry):
        entry = re.sub(r'/$', '', entry)
        if self.version_prefix:
            entry = re.sub(r'^' + re.escape(self.version_prefix), '', entry)
        if self.version_suffix:
            entry = re.sub(re.escape(self.version_suffix) + r'$', '', entry)
        return Version(entry, partial=True)

    def fetch(self, version=None):
        _cwd, listing = htmllistparse.fetch_listing(self.url)
        for e in listing:
            try:
                semver = self.__parse_entry(e.name)
                if version == None or semver > Version(version, partial=True):
                    self.versions.add(semver)
            except ValueError:
                print('Ignoring invalid version:', e.name, file=sys.stderr)

    def to_json(self):
        output = []
        for v in sorted(self.versions):
            output.append({"version": str(v)})
        return output
