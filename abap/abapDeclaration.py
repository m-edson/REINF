_ttypes = dict([(1, 'TYPE'), (2, 'TYPE REF TO'), (3, 'TYPE TABLE OF'), (4, 'LIKE LINE OF'), (5, 'LIKE')])
_prefix = dict([(1, 'DATA'), (2, 'FIELD_SYMBOL'), (3, '')])


class AbapDeclarationTTypes:
    def __init__(self, parent):
        # type: (AbapDeclarationBuilder) -> ()
        self.parent = parent

    def type(self):
        self.parent._declaration.ttype = 1
        return self.parent

    def type_ref_to(self):
        self.parent._declaration.ttype = 2
        return self.parent

    def type_table_of(self):
        self.parent._declaration.ttype = 3
        return self.parent

    def like_line_of(self):
        self.parent._declaration.ttype = 4
        return self.parent

    def like(self):
        self.parent._declaration.ttype = 5
        return self.parent


class AbapDeclaration:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.ttype = 0
        self.prefix = 1

    def __str__(self):
        return _prefix[self.prefix] + ' ' + self.name + ' ' + _ttypes[self.ttype] + ' ' + self.type + '.'


class AbapDeclarationBuilder:
    def __init__(self):
        self._dec_ttypes = AbapDeclarationTTypes(self)
        self._declaration = AbapDeclaration()
        self._declaration.prefix = 1
        self._declaration.ttype = 1

    def set_name(self, name):
        # type: (str) -> AbapDeclarationBuilder
        self._declaration.name = name
        return self

    def set_type(self, type):
        # type: (str) -> AbapDeclarationBuilder
        self._declaration.type = type
        return self

    def set_prefix(self, prefix):
        # type: (str) -> AbapDeclarationBuilder
        self._declaration.prefix = prefix
        return self

    def set_ttype(self):
        # type: (name) -> AbapDeclarationTTypes
        return self._dec_ttypes

    def build(self):
        # type: () -> AbapDeclaration
        return self._declaration
