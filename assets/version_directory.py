import requests
from urllib.parse import urljoin
from directory import Directory
from hash_parser import HashParser

class VersionDirectory(Directory):
    def __init__(self, source, version):
        super(VersionDirectory, self).__init__(source)
        self.version = version
        hash_format = 'mds'
        self.hash_algorithm = 'sha1'
        if 'hash-format' in source:
            hash_format = source['hash-format']
        if 'hash-algorithm' in source:
            self.hash_algorithm = source['hash-algorithm']
        self.hash_parser = HashParser(hash_format)
        self.version_dir = self.__join_strings([self.version_prefix, self.version])
        self.hash_file = self.__join_strings([self.hash_prefix, self.version, self.hash_suffix])
        self.bin_file = self.__join_strings([self.bin_prefix, self.version, self.bin_suffix])
        self.source_file = self.__join_strings([self.source_prefix, self.version, self.source_suffix])

    def fetch_hash(self):
        hash_url = urljoin(self.url, self.version_dir + "/" + self.hash_file)
        req = requests.get(hash_url, timeout=30)
        req.raise_for_status()
        self.hash_parser.parse(req.content.decode('utf-8'))
        return self.hash_parser.get(self.bin_file, self.hash_algorithm)

    def bin_url(self):
        return urljoin(self.url, self.version_dir + "/" + self.bin_file)

    def source_url(self):
        return urljoin(self.url, self.version_dir + "/" + self.source_file)

    def __join_strings(self, string_list):
        ret = ""
        for i in string_list:
            if i:
                ret += i
        return ret
