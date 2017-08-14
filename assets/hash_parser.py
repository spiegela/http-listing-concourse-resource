import re
import sys

class HashParser(object):

    def __init__(self, hash_format):
        self.hash_format = hash_format
        self.hash_dict = {}

    def parse(self, content):
        parse_methods = {
            'mds':  self.parse_mds,
            'md5':  self.parse_md5,
            'sha1': self.parse_sha1
        }
        parse_methods[self.hash_format](content)

    def get(self, filename, hash_algorithm):
        if filename in self.hash_dict:
            if hash_algorithm in self.hash_dict[filename]:
                return self.hash_dict[filename][hash_algorithm]
        return None

    def parse_mds(self, content):
        fname = None
        htype = None
        for line in content.split('\n'):
            empty = re.match(r'^\s*$', line)
            m = re.match(r'^(.+):\s+([A-Z|0-9]+)\s+=\s+((\w|\d|\s)+)$', line)
            m2 = re.match(r'\s+((\w|\d|\s)+)$', line)
            if empty:
                next
            elif m:
                fname = m.group(1)
                htype = m.group(2).lower()
                hvalue = re.sub('\s', '', m.group(3).lower())
                if fname in self.hash_dict:
                    self.hash_dict[fname][htype] = hvalue
                else:
                    self.hash_dict[fname] = {htype: hvalue}
            elif m2 and fname and htype:
                hvalue = re.sub('\s', '', m2.group(1).lower())
                self.hash_dict[fname][htype] += hvalue
            else:
                print('Unable to parse line: ', line, file=sys.stderr)

    def parse_sha1(self, content):
        (fname, hvalue) = HashParser.__hash_space_fname(content)
        self.hash_dict[fname] = {'sha1': hvalue}

    def parse_md5(self, content):
        (fname, hvalue) = HashParser.__hash_space_fname(content)
        self.hash_dict[fname] = {'md5': hvalue}

    def __hash_space_fname(content):
        for line in content.split('\n'):
            empty = re.match(r'^\s*$', line)
            m = re.match(r'^((\w|\d)+) +(.+)$', line)
            if empty:
                next
            elif m:
                return (m.group(3), m.group(1))
            else:
                print('Unable to parse line: ', line, file=sys.stderr)
