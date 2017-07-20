from abapClassMethod import *
from abapDeclaration import *


class AbapClassSession:
    _allowed_type = ['PUBLIC', 'PROTECTED', 'PRIVATE']

    def __init__(self):
        self.type = ''
        self.methods = list()
        self.declaration = list()

    def __str__(self):
        s = self.type + ' SESSION.\n'
        for d in self.declaration:
            s += str(d) + '\n'

        for m in self.methods:
            s += m.declaration()
        return s

    def set_session_type(self, session_type):
        if not AbapClassSession._allowed_type.__contains__(session_type):
            raise ValueError('Valid Values = ' + str(AbapClassSession._allowed_type))
        self.type = session_type


class AbapClassSessionBuilder:
    def __init__(self):
        self._session = AbapClassSession()

    def set_session_type(self, session_type):
        self._session.set_session_type(session_type)
        return self

    def add_method(self, method):
        # type: (AbapClassMethod) -> AbapClassSessionBuilder
        self._session.methods.append(method)
        return self

    def add_declaration(self, declaration):
        # type: (AbapDeclaration) -> AbapClassSessionBuilder
        self._session.declaration.append(declaration)
        return self

    def build(self):
        return self._session


def create(obj):
    return obj.build()


method = create(AbapClassMethodBuilder()
                .set_method_name('Method 1')
                .add_importing_param(AbapDeclarationBuilder()
                                     .set_name('var1')
                                     .set_type('BUKRS')
                                     .set_prefix(3)
                                     .build())
                .add_importing_param(AbapDeclarationBuilder()
                                     .set_name('var2')
                                     .set_type('BRANCH')
                                     .set_prefix(3)
                                     .build())
                .add_code(['WRITE: \'Hello World\'']))

var = create(AbapClassSessionBuilder()
             .set_session_type('PUBLIC')
             .add_method(method))

print str(var)
