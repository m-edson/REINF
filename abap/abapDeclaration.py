_ttypes = dict([(1, 'TYPE'), (2, 'TYPE REF TO'), (3, 'TYPE TABLE OF'), (4, 'LIKE LINE OF'), (5, 'LIKE'), (6, '')])
_prefix = dict([(1, 'DATA'), (2, 'FIELD_SYMBOL'), (3, '')])


class AbapDeclaration:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.ttype = ''
        self.prefix = ''

    def __str__(self):
        return _prefix[self.prefix] + ' ' + self.name + ' ' + _ttypes[self.ttype] + ' ' + self.type + '.'


class AbapDeclarationBuilder:
    def __init__(self):
        self._declaration = AbapDeclaration()
        self._declaration.prefix = 1
        self._declaration.ttype = 1
        self._dot = True

    def set_name(self, name):
        # type: (name) -> AbapDeclarationBuilder
        self._declaration.name = name
        return self

    def set_type(self, type):
        # type: (name) -> AbapDeclarationBuilder
        self._declaration.type = type
        return self

    def set_prefix(self, prefix):
        # type: (name) -> AbapDeclarationBuilder
        self._declaration.prefix = prefix
        return self

    def set_ttype(self, ttype):
        # type: (name) -> AbapDeclarationBuilder
        self._declaration.ttype = ttype
        return self

    def dot(self, dot=True):
        self._dot = dot

    def build(self):
        # type: () -> AbapDeclaration
        return self._declaration
