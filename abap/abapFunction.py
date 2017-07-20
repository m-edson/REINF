from abapCommand import AbapCommand

__function_types = [(1, 'FORM'), (2, 'FUNCTION'), (3, 'METHOD')]


class AbapFunctionBuilder:
    def __init__(self):
        self._abapFunction = AbapFunction()

    def build(self):
        pass

    def add_exporting_param(self, param, value):
        # type: (str,str) -> AbapFunction
        self._abapFunction.exp_param.add((param, value))
        return self

    def add_importing_param(self, param, value):
        # type: (str,str) -> AbapFunction
        self._abapFunction.imp_param.add((param, value))
        return self

    def add_changing_param(self, param, value):
        # type: (str,str) -> AbapFunction
        self._abapFunction.changing_param.add((param, value))
        return self

    def add_using_param(self, param, value):
        # type: (str,str) -> AbapFunction
        self._abapFunction.changing_param.add((param, value))
        return self

    def add_table_param(self, param, value):
        # type: (str,str) -> AbapFunction
        self._abapFunction.table_param.add((param, value))
        return self

    def add_exception(self, name):
        # type: (str,int) -> AbapFunction
        ret_value = len(self._abapFunction.exceptions) + 1
        self._abapFunction.exceptions.append((name, ret_value))
        return self

    def set_subrc_check(self, check):
        # type: (bool) -> ()
        self._subrc_check = check


class AbapFunction(AbapCommand):
    def __init__(self, func_name='', func_type=1):
        AbapCommand.__init__(self)
        self.type = func_type
        self.func_name = func_name
        self.exp_param = set()
        self.imp_param = set()
        self.changing_param = set()
        self.table_param = set()
        self.using_param = set()
        self.exceptions = list()
        self.subrc_check = False
        self.code = list()

# def add_exporting_param(self, param, value):
#         # type: (str,str) -> AbapFunction
#         self._exp_param.add((param, value))
#         return self
#
#     def add_importing_param(self, param, value):
#         # type: (str,str) -> AbapFunction
#         self._imp_param.add((param, value))
#         return self
#
#     def add_changing_param(self, param, value):
#         # type: (str,str) -> AbapFunction
#         self._changing_param.add((param, value))
#         return self
#
#     def add_table_param(self, param, value):
#         # type: (str,str) -> AbapFunction
#         self._table_param.add((param, value))
#         return self
#
#     def add_exception(self, name):
#         # type: (str,int) -> AbapFunction
#         ret_value = len(self._exceptions) + 1
#         self._exceptions.append((name, ret_value))
#         return self
#
#
# def set_subrc_check(self, check):
#     # type: (bool) -> ()
#     self._subrc_check = check
#
#
# def _add_subrc_check(self):
#     self._add_command('IF sy-subrc <> 0.')
#     self._add_command(
#         'MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
#     self._add_command('ENDIF.')
#
#
# def build_command(self):
#     self._add_command('CALL FUNCTION \'' + self.func_name + '\'')
#
#     if self._exp_param:
#         self._add_command('EXPORTING')
#         for p in self._exp_param:
#             self._add_command(p[0] + ' = ' + p[1])
#
#     if self._imp_param:
#         self._add_command('IMPORTING')
#         for p in self._exp_param:
#             self._add_command(p[0] + ' = ' + p[1])
#
#     if self._changing_param:
#         self._add_command('CHANGING')
#         for p in self._exp_param:
#             self._add_command(p[0] + ' = ' + p[1])
#
#     if self._table_param:
#         self._add_command('TABLES')
#         for p in self._exp_param:
#             self._add_command(p[0] + ' = ' + p[1])
#
#     if self._exceptions:
#         self._add_command('EXCEPTIONS')
#         for p in self._exp_param:
#             self._add_command(p[0] + ' = ' + p[1])
#
#     if self._subrc_check:
#         self._add_subrc_check()
