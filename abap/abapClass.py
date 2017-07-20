from abapClassSession import *


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
        if self.parent_class != '':
            s += 'INHERITING FROM ' + self.parent_class + '\n'
        if self.final:
            s += 'FINAL\n'
        elif self.abstract:
            s += 'ABSTRACT\n'
        s += 'CREATE PUBLIC.\n'

        s += str(self.public_session.build())
        s += str(self.protected_session.build())
        s += str(self.public_session.build())

        s += 'ENDCLASS.\n\n'

        s += 'CLASS ' + str(self.name) + ' IMPLEMENTATION.'

        for m in self.public_session.build().methods:
            s += m.implementation()

        for m in self.protected_session.build().methods:
            s += m.implementation()

        for m in self.private_session.build().methods:
            s += m.implementation()

        s += 'ENDCLASS.'


class AbapClassBuilder:
    def __init__(self):
        self._abap_class = AbapClass()
        self._private_session_builder = AbapClassSessionBuilder()
        self._protected_session_builder = AbapClassSessionBuilder()
        self._public_session_builder = AbapClassSessionBuilder()

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
        self._abap_class = final
        if final:
            self._abap_class.abstract = False
        return self

    def private_session(self):
        # type: (str) -> AbapClassSessionBuilder
        return self._private_session_builder

    def protected_session(self):
        # type: (str) -> AbapClassSessionBuilder
        return self._protected_session_builder

    def public_session(self):
        # type: (str) -> AbapClassSessionBuilder
        return self._public_session_builder
