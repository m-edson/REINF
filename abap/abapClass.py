from abapClassSection import *


class AbapClass:
    def __init__(self, class_name='', parent_class=''):
        self.name = class_name
        self.parent_class = parent_class
        self.abstract = False
        self.final = False
        self.private_session = None
        self.protected_session = None
        self.public_session = None

    def __str__(self):
        s = 'CLASS ' + str(self.name) + ' DEFINITION\n'
        s += 'PUBLIC\n'
        if self.parent_class != '':
            s += 'INHERITING FROM ' + self.parent_class + '\n'
        if self.final:
            s += 'FINAL\n'
        elif self.abstract:
            s += 'ABSTRACT\n'
        s += 'CREATE PUBLIC.\n\n'

        if self.public_session is not None:
            s += str(self.public_session)
        if self.protected_session is not None:
            s += str(self.protected_session)
        if self.private_session is not None:
            s += str(self.private_session)

        s += 'ENDCLASS.\n\n'

        s += 'CLASS ' + str(self.name) + ' IMPLEMENTATION.\n'

        if self.public_session is not None:
            for m in self.public_session.methods:
                s += m.implementation()

        if self.protected_session is not None:
            for m in self.protected_session.methods:
                s += m.implementation()

        if self.private_session is not None:
            for m in self.private_session.methods:
                s += m.implementation()

        s += '\nENDCLASS.'

        return s


class AbapClassBuilder:
    def __init__(self):
        self._abap_class = AbapClass()

    @staticmethod
    def create(abap_class_builder):
        # self: (AbapClassBuilder) -> AbapClass
        return abap_class_builder.build()

    def build(self):
        # type: () -> AbapClass
        return self._abap_class

    def set_class_name(self, name):
        # type: (str) -> AbapClassBuilder
        self._abap_class.name = name
        return self

    def set_parent_class(self, parent_class):
        # type: (str) -> AbapClassBuilder
        self._abap_class.parent_class = parent_class
        return self

    def set_abstract(self, abstract=True):
        # type: (bool) -> AbapClassBuilder
        self._abap_class.abstract = abstract
        if abstract:
            self._abap_class.final = False
        return self

    def set_final(self, final=True):
        # type: (bool) -> AbapClassBuilder
        self._abap_class.final = final
        if final:
            self._abap_class.abstract = False
        return self

    def set_private_session(self, class_session):
        # type: (AbapClassSection) -> AbapClassBuilder
        self._abap_class.private_session = class_session
        return self

    def set_protected_session(self, class_session):
        # type: (AbapClassSection) -> AbapClassBuilder
        self._abap_class.protected_session = class_session
        return self

    def set_public_session(self, class_session):
        # type: (AbapClassSection) -> AbapClassBuilder
        self._abap_class.public_session = class_session
        return self

# def create(obj):
#     return obj.build()
#
#
# method = create(AbapClassMethodBuilder()
#                 .set_method_name('Method_1')
#                 .add_importing_param(AbapDeclarationBuilder()
#                                      .set_name('var1')
#                                      .set_type('BUKRS')
#                                      .set_prefix(3)
#                                      .build())
#                 .add_importing_param(AbapDeclarationBuilder()
#                                      .set_name('var2')
#                                      .set_type('J_1BBRANC_')
#                                      .set_prefix(3)
#                                      .build())
#                 .add_code(['WRITE: \'Hello World\'.']))
#
# session = create(AbapClassSectionBuilder()
#                  .set_session_type('PUBLIC')
#                  .add_method(method))
#
# _class = create(AbapClassBuilder()
#                 .set_class_name('Z_CLASS_TESTE')
#                 .set_final()
#                 .set_private_session(session))
#
# print str(_class)
