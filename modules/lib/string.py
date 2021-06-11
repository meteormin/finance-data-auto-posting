import re

class Str:
    @staticmethod
    def snake(s: str):
        """ 
        Is it ironic that this function is written in camel case, yet it
        converts to snake case? hmm..
        """
        underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
        underscorer2 = re.compile('([a-z0-9])([A-Z])')

        subbed = underscorer1.sub(r'\1_\2', s)
        return underscorer2.sub(r'\1_\2', subbed).lower()

    @staticmethod
    def camel(s: str):
        return s.title().replace('_', '')
