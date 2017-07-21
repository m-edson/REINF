from abapDeclaration import *


class AbapClassMethod:
    def __init__(self):
        self.name = ''
        self.exp_param = set()
        self.imp_param = set()
        self.changing_param = set()
        self.ret_param = None
        self.exceptions = list()
        self.code = list()

    def declaration(self):
        # type: () -> str
        s = '\nMETHODS: ' + self.name + '\n'
        if self.imp_param:
            s += '\tIMPORTING\n'
            for p in self.imp_param:
                s += '\t\t' + str(p).replace('.', '') + '\n'

        if self.exp_param:
            s += '\tEXPORTING\n'
            for p in self.exp_param:
                s += '\t\t' + str(p).replace('.', '') + '\n'

        if self.changing_param:
            s += '\tCHANGING\n'
            for p in self.changing_param:
                s += '\t\t' + str(p).replace('.', '') + '\n'

        if self.ret_param is not None:
            s += '\tRETURING\n'
            s += '\t\t' + str(self.ret_param).replace('.', '') + '\n'

        if self.exceptions:
            s += '\tEXCEPTIONS\n'
            for e in self.exceptions:
                s += '\t\t' + str(e[0]) + ' = ' + str(e[1]) + '\n'

        s = s[:-1]
        s += '.\n\n'
        # s = s[-1:]
        # s += '.\n'

        return s

    def implementation(self):
        # type: () -> str

        s = '\nMETHOD ' + self.name + '.\n\n'
        for line in self.code:
            s += line.strip() + '\n'
        s += '\nENDMETHOD.\n'
        return s


class AbapClassMethodBuilder:
    def __init__(self):
        self._class_method = AbapClassMethod()

    def set_method_name(self, name):
        # type: (str) -> AbapClassMethodBuilder
        self._class_method.name = name
        return self

    def add_exporting_param(self, param):
        # type: (AbapDeclaration) -> AbapClassMethodBuilder
        self._class_method.exp_param.add(param)
        return self

    def add_importing_param(self, param):
        # type: (AbapDeclaration) -> AbapClassMethodBuilder
        self._class_method.imp_param.add(param)
        return self

    def add_changing_param(self, param):
        # type: (AbapDeclaration) -> AbapClassMethodBuilder
        self._class_method.changing_param.add(param)
        return self

    def def_returning_param(self, param):
        # type: (AbapDeclaration) -> AbapClassMethodBuilder
        self._class_method.ret_param = param
        return self

    def add_exception(self, exception):
        # type: (str) -> AbapClassMethodBuilder
        except_value = len(self._class_method.exceptions)
        self._class_method.exceptions.append((exception, except_value))
        return self

    def add_code(self, code):
        # type: ([str]) -> AbapClassMethodBuilder
        self._class_method.code += code
        return self

    def build(self):
        return self._class_method
