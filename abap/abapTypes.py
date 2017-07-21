from abapDeclaration import *


class AbapTypes:
    def __init__(self, name=''):
        # type: (str) -> AbapTypes
        self.name = name
        self.prefix = ''
        self.types = []

    def __str__(self):
        if self.prefix == 'TYPES: BEGIN OF':
            s = self.prefix + ' ' + self.name + ',\n'

            for t in self.types:
                s += '\t' + str(t).replace('.', ',') + '\n'
            s += 'END OF ' + self.name + '.\n'
            return s
        else:
            return self.prefix + ' ' + self.name + ' ' + str(self.types[0]).replace('.',
                                                                                    '') + ' WITH NON-UNIQUE DEFAULT KEY.\n'


class AbapTypesBuilder:
    def __init__(self):
        self._types = AbapTypes()

    def create_types_begin_of(self, name):
        # type: (str) -> AbapTypesBuilder
        self._set_name(name)
        self._set_prefix('TYPES: BEGIN OF')
        return self

    def cretate_types(self):
        # type: (str) -> AbapTypesBuilder
        self._set_prefix('TYPES:')
        return self

    def _set_name(self, name):
        # type: (str) -> AbapTypesBuilder
        self._types.name = name
        return self

    def _set_prefix(self, prefix):
        # type: (int) -> AbapTypesBuilder
        self._types.prefix = prefix
        return self

    def add_declaration(self, declaration):
        # type: (AbapDeclaration) -> AbapTypesBuilder
        declaration.prefix = 3
        self._types.types.append(declaration)
        return self

    def build(self):
        # type: () -> AbapTypes
        return self._types
