class Directory(object):
    def __init__(self, source):
        self.url = source['url']
        if 'url-params' in source:
            self.url_params = source['url-params']
        else:
            self.url_params = None
        self.version_prefix = self.__get_param('version', 'prefix', source)
        self.version_suffix = self.__get_param('version', 'suffix', source)
        self.hash_prefix = self.__get_param('hash', 'prefix', source)
        self.hash_suffix = self.__get_param('hash', 'suffix', source)
        self.bin_prefix = self.__get_param('bin', 'prefix', source)
        self.bin_suffix = self.__get_param('bin', 'suffix', source)
        self.source_prefix = self.__get_param('source', 'prefix', source)
        self.source_suffix = self.__get_param('source', 'suffix', source)

    def __get_param(self, attribute, modifier_type, source):
        param = str.join('-', [attribute, modifier_type])
        if param in source:
            return source[param]
        elif modifier_type in source:
            return source[modifier_type]
