from abapClassMethod import *
from abapDeclaration import *


class AbapClassSection:
    _allowed_type = ['PUBLIC', 'PROTECTED', 'PRIVATE']

    def __init__(self):
        self.type = ''
        self.methods = list()
        self.declaration = list()

    def __str__(self):
        s = self.type + ' SECTION.\n'
        for d in self.declaration:
            s += str(d) + '\n'

        for m in self.methods:
            s += m.declaration()
        return s

    def set_session_type(self, session_type):
        if not AbapClassSection._allowed_type.__contains__(session_type):
            raise ValueError('Valid Values = ' + str(AbapClassSection._allowed_type))
        self.type = session_type


class AbapClassSectionBuilder:
    def __init__(self):
        self._session = AbapClassSection()

    def set_session_type(self, session_type):
        self._session.set_session_type(session_type)
        return self

    def add_method(self, method):
        # type: (AbapClassMethod) -> AbapClassSectionBuilder
        self._session.methods.append(method)
        return self

    def add_declaration(self, declaration):
        # type: (AbapDeclaration) -> AbapClassSectionBuilder
        self._session.declaration.append(declaration)
        return self

    def create_public_session(self):
        # type: () -> AbapClassSectionBuilder
        self.set_session_type('PUBLIC')
        return self

    def create_protected_session(self):
        # type: () -> AbapClassSectionBuilder
        self.set_session_type('PROTECTED')
        return self

    def create_private_session(self):
        # type: () -> AbapClassSectionBuilder
        self.set_session_type('PRIVATE')
        return self

    def build(self):
        return self._session
