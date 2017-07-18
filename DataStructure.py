def camel_case_to_underscore(text):
    l = map(lambda x: x if x.islower() else "_" + x, text)

    underscore = [l[0]]

    for i in range(1, len(l) - 1):
        if l[i].startswith('_') and l[i - 1].startswith('_') and l[i + 1].isupper():
            underscore.append(l[i].replace('_', ''))
        else:
            underscore.append(l[i])

    last = l[len(l) - 1]
    if last.startswith('_'):
        last = last[1:]

    underscore.append(last)

    value = ''.join(underscore).upper()
    if value.startswith('_'):
        value = value[1:]

    return value


basic_types = ['Z_REINF_PERIODO', 'Z_REINF_TEXTO', 'Z_REINF_NUMERO', 'Z_REINF_VALOR', 'Z_REINF_DATA']


def cat_tab_info(tab_cat_name, struct_name, descricao):
    command = []
    command.append('wa_dd40v-typename = \'Y' + tab_cat_name + '\'.')
    command.append('wa_dd40v-rowtype = \'Y' + struct_name + '\'.')
    command.append('wa_dd40v-ddlanguage = sy-langu.')
    command.append('wa_dd40v-rowkind = \'S\'.')
    command.append('wa_dd40v-accessmode = \'T\'.')
    command.append('wa_dd40v-keydef = \'D\'.')
    command.append('wa_dd40v-ddtext = \'' + descricao + '\'.')
    command.append('wa_dd40v-as4user = sy-uname.')
    command.append('wa_dd40v-as4date = sy-datum.')
    command.append('wa_dd40v-as4time = sy-uzeit.')
    return command


def cat_tab_put(tab_cat_name):
    command = []
    command.append('CALL FUNCTION \'DDIF_TTYP_PUT\'')
    command.append('EXPORTING')
    command.append('name = \'Y' + tab_cat_name + '\'')
    command.append('dd40v_wa          = wa_dd40v')
    command.append('EXCEPTIONS')
    command.append('ttyp_not_found    = 1')
    command.append('name_inconsistent = 2')
    command.append('ttyp_inconsistent = 3')
    command.append('put_failure       = 4')
    command.append('put_refused       = 5')
    command.append('OTHERS = 6.')
    command.append('IF sy-subrc <> 0.')
    command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
    command.append('ENDIF.')
    return command


def cat_tab_activate(tab_cat_name):
    command = []
    command.append('CALL FUNCTION \'DDIF_TTYP_ACTIVATE\'')
    command.append('EXPORTING')
    command.append('name        = \'Y' + tab_cat_name + '\'')
    command.append('EXCEPTIONS')
    command.append('not_found   = 1')
    command.append('put_failure = 2')
    command.append('OTHERS      = 3.\n')
    command.append('IF sy-subrc <> 0.')
    command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
    command.append('ENDIF.\n')
    command.append('CLEAR wa_dd40v.')
    return command


def struct_line(tab_name, field_name, type_name, position):
    # type: (str,str,str,int) -> [str]

    if not basic_types.__contains__(type_name):
        type_name = 'Y' + type_name

    command = []
    command.append('CLEAR idd03p.')
    command.append('idd03p-tabname  = \'Y' + tab_name + '\'.')
    command.append('idd03p-fieldname = \'' + field_name + '\'.')
    command.append('idd03p-rollname = \'' + type_name + '\'.')
    command.append('idd03p-position = \'' + str(position) + '\'.')
    command.append('APPEND idd03p.')
    return command


def struct_def(tab_name, description):
    # type: (str,str,str,str,str) -> [str]
    command = []
    command.append('xdd02v-tabname = \'Y' + tab_name + '\'.')
    command.append('xdd02v-tabclass = \'INTTAB\'.')
    command.append('xdd02v-ddlanguage =  sy-langu.')
    command.append('xdd02v-langdep =  sy-langu.')
    command.append('xdd02v-ddtext  = \'' + description + '\'.')
    return command


def tabl_put(tab_name):
    # type: (str) -> [str]
    command = []
    command.append('CALL FUNCTION \'DDIF_TABL_PUT\'')
    command.append('EXPORTING')
    command.append('name = \'Y' + tab_name + '\'')
    command.append('dd02v_wa          = xdd02v')
    command.append('TABLES')
    command.append('dd03p_tab         = idd03p')
    command.append('EXCEPTIONS')
    command.append('tabl_not_found    = 1')
    command.append('name_inconsistent = 2')
    command.append('tabl_inconsistent = 3')
    command.append('put_failure       = 4')
    command.append('put_refused       = 5')
    command.append('OTHERS            = 6.\n')
    command.append('IF sy-subrc <> 0.')
    command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
    command.append('ENDIF.')
    return command


def tabl_activate(tab_name):
    command = []
    command.append('CALL FUNCTION \'DDIF_TABL_ACTIVATE\'')
    command.append('EXPORTING')
    command.append('name        = \'Y' + tab_name + '\'')
    command.append('EXCEPTIONS')
    command.append('not_found   = 1')
    command.append('put_failure = 2')
    command.append('OTHERS      = 3.\n')
    command.append('IF sy-subrc <> 0.')
    command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
    command.append('ENDIF.\n')
    command.append('CLEAR idd03p[].')
    return command


def init_ddic():
    ddic = dict()
    ddic['ACCP'] = 'Z_REINF_PERIODO'

    ddic['STRG'] = 'Z_REINF_TEXTO'
    ddic['xs:ID'] = 'Z_REINF_TEXTO'

    ddic['NUMC'] = 'Z_REINF_NUMERO'

    ddic['DEC'] = 'Z_REINF_VALOR'

    ddic['DATS'] = 'Z_REINF_DATA'
    return ddic


class DataStructure:
    ddic = init_ddic()

    def __init__(self):
        self._children = []
        self._parent = None
        self.name = ''
        self.version = ''
        self._types = []
        self.xml_node = None

        self.level = 0
        self.var_name = ''
        self.xml_name = ''
        self.xml_type = ''
        self.min_occurs = 0
        self.max_occurs = 0
        self.min_length = 0
        self.max_length = 0
        self.pattern = ''
        self.data_type = ''

    def get_children_nodes(self):
        # type: () -> [DataStructure]
        return self._children

    def get_types(self):
        # type: () -> [DataStructure]
        return self._types

    def append_child(self, ds):
        # type: (DataStructure) -> ()
        self._children.append(ds)
        ds._parent = self

    def append_type_ref(self, ds):
        # type: (DataStructure) -> ()
        self._types.append(ds)

    def get_parent(self):
        # type: () -> DataStructure
        return self._parent

    def set_event_name(self, name):
        # type: (str) -> ()
        self.name = name

    def set_event_version(self, version):
        # type: (str) -> ()
        self.version = version

    # def bfs(self, queue=None):
    #     # type: (deque) -> list
    #
    #     stack = []
    #
    #     if queue is None:
    #         queue = deque([self])
    #
    #     while len(queue) > 0:
    #         node = queue.popleft()
    #         stack.append(node)
    #         for n in node.get_children_nodes():
    #             queue.append(n)
    #         stack += self.bfs(queue)
    #
    #     return stack
    #
    # def reverse_bfs(self, node_queue=None):
    #     # type: (deque) -> ()
    #     if node_queue is None:
    #         node_queue = deque([self])
    #
    #     node_queue.append(self)
    #     for node in self.get_children_nodes():
    #         node.reverse_bfs(node_queue)
    #
    #     return node_queue

    def write_ddic_generator(self, write=True, command_stack=[]):
        # type: (bool,list) -> ()

        if self.var_name == 'REINF':
            self.get_children_nodes()[0].write_ddic_generator(False, command_stack)
        else:

            if self.xml_type == 'G':
                if self.max_occurs > 1:
                    tab_cat_name = self.var_name + '_T'
                    command_stack.append(cat_tab_activate(tab_cat_name))
                    command_stack.append(cat_tab_put(tab_cat_name))
                    command_stack.append(cat_tab_info(tab_cat_name, self.var_name, 'PYGEN'))

                command_stack.append(tabl_activate(self.var_name))
                command_stack.append(tabl_put(self.var_name))
                command_stack.append(struct_def(self.var_name, 'PYGEN'))

                count = 1
                for n in self.get_children_nodes():
                    if n.max_occurs > 1:
                        tab_cat_name = n.var_name + '_T'
                        command_stack.append(struct_line(self.var_name, n.var_name, tab_cat_name, count))
                    else:
                        command_stack.append(struct_line(self.var_name, n.var_name, n.get_ddic_type(), count))
                    count += 1
            # elif self.xml_type == 'E' or 'A':
            #     index = self.get_parent().get_children_nodes().index(self)
            #     command_stack.append(
            #         struct_line(self.get_parent().var_name, self.var_name, self.get_ddic_type(), index))

            for n in self.get_children_nodes():
                n.write_ddic_generator(False, command_stack)

        if write is True:
            f = open('output/ddic_' + self.name + '-' + self.version + '.abap', 'w')

            f.write('REPORT ZPYGEN.\n')
            f.write('DATA: xdd02v TYPE dd02v.\n')
            f.write('DATA: idd03p TYPE TABLE OF dd03p WITH HEADER LINE.\n')
            f.write('DATA: name     TYPE ddobjname.\n')
            f.write('DATA: wa_dd40v TYPE dd40v.\n')
            f.write('START-OF-SELECTION.\n\n')

            while command_stack:
                command = command_stack.pop()
                for c in command:
                    f.write(c)
                    f.write('\n')
                f.write('\n')
            f.close()

    def resolve_type_references(self, types, type_names=None):
        # type: () -> ()

        if type_names is None:
            type_names = [x.xml_name for x in types]

        for node in self._children:
            if type_names.__contains__(node.data_type):
                node._children = types[type_names.index(node.data_type)].get_children_nodes()
                node.data_type = camel_case_to_underscore(node.xml_name)
                node.xml_type = 'G'
            node.resolve_type_references(types, type_names)

    def write_method_file(self, f=None, level=-1):
        # type: (file, int) -> ()

        if level == -1:
            path = 'output/' + self.name + '_' + self.version + '.abap'
            f = open(path, 'w')

            f.write('METHOD create_out_format.\n')
            f.write('DATA: lw_out_format TYPE zsoutputformat.\n\n')

            f.write('DEFINE monta_formatador_1.\n\n')

            f.write('lw_out_format-level = &1.\n')
            f.write('lw_out_format-var_name = &2.\n')
            f.write('lw_out_format-xml_name = &3.\n')
            f.write('lw_out_format-xml_type = &4.\n')
            f.write('lw_out_format-min_occurs = &5.\n')
            f.write('lw_out_format-max_occurs = &6.\n')
            f.write('lw_out_format-min_length = &7.\n')
            f.write('lw_out_format-max_length = &8.\n')
            f.write('lw_out_format-pattern = &9.\n\n')

            f.write('END-OF-DEFINITION.\n\n')

            f.write('DEFINE monta_formatador_2.\n\n')
            f.write('lw_out_format-datatype = &1.\n')
            f.write('APPEND lw_out_format TO ct_out_format.\n')
            f.write('CLEAR lw_out_format.\n\n')
            f.write('END-OF-DEFINITION.\n\n')

        f.write(
            'monta_formatador_1 ' + str(level) + ' \'' + str(self.var_name) + '\'' + ' \'' + str(self.xml_name) + '\'' +
            ' \'' + str(self.xml_type) + '\' ' + str(self.min_occurs) + ' ' + str(self.max_occurs) + ' ' +
            str(self.min_length) + ' ' + str(self.max_length) + ' ' +
            '\'' + str(self.pattern) + '\'' + '.\n')
        f.write('monta_formatador_2 ' + '\'' + str(self.data_type) + '\'' + '.\n\n')

        for child in self._children:
            child.write_method_file(f, level + 1)

        if level == -1:
            f.write('ENDMETHOD.\n')
            f.close()

    def write_ddic_gen_file(self, f=None, level=-1):
        # type: (file) -> ()

        path = ''

        if level == -1:
            path = 'output/dg_' + self.name + '_' + self.version + '.abap'
            f = open(path, 'w')

        result = True

        report_name = path.replace('output/', '')
        report_name = report_name.replace('.abap', '')

        tab_name = 'ZPY_' + self.var_name

        for node in self._children:
            result = result and (len(node.get_children_nodes()) == 0)

        if level == -1:
            f.write('REPORT ' + report_name + '.\n')
            f.write('DATA: xdd02v TYPE dd02v.\n')
            f.write('DATA: idd03p TYPE TABLE OF dd03p WITH HEADER LINE.\n')
            f.write('START-OF-SELECTION.\n\n')

        if result is False:
            for node in self._children:
                node.write_ddic_gen_file(f, level + 1)

        f.write('CLEAR xdd02v.\n')
        f.write('xdd02v-tabname = ' + tab_name + '.\n')
        f.write('xdd02v-tabclass = INTTAB.\n')
        f.write('xdd02v-ddlanguage = sy-langu.\n')
        f.write('xdd02v-langdep = sy-langu.\n')
        f.write('xdd02v-ddtext  = PyGen.\n\n')

        i = 1
        for node in self._children:
            f.write('CLEAR idd03p.\n')
            f.write('idd03p-tabname  = ' + tab_name + '.\n')
            f.write('idd03p-fieldname = \'' + node.var_name + '\'.\n')
            f.write('idd03p-rollname = ' + node.get_ddic_type() + '.\n')
            f.write('idd03p-position = ' + str(i) + '.\n')
            f.write('APPEND idd03p.\n\n')
            i += 1

        f.write('CALL FUNCTION \'DDIF_TABL_PUT\'\n'
                '    EXPORTING\n'
                '       name             = ' + tab_name + '\n'
                                                          '      dd02v_wa          = xdd02v\n'
                                                          '    TABLES\n'
                                                          '      dd03p_tab         = idd03p\n'
                                                          '    EXCEPTIONS\n'
                                                          '      tabl_not_found    = 1\n'
                                                          '      name_inconsistent = 2\n'
                                                          '      tabl_inconsistent = 3\n'
                                                          '      put_failure       = 4\n'
                                                          '      put_refused       = 5\n'
                                                          '      OTHERS            = 6.\n'
                                                          '\n'
                                                          '  IF sy-subrc <> 0.\n'
                                                          '    MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno\n'
                                                          '            WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.\n'
                                                          '  ENDIF.\n'
                                                          '  CALL FUNCTION \'DDIF_TABL_ACTIVATE\'\n'
                                                          '    EXPORTING\n'
                                                          '      name        = ' + tab_name + '\n'
                                                                                              '    EXCEPTIONS\n'
                                                                                              '      not_found   = 1\n'
                                                                                              '      put_failure = 2\n'
                                                                                              '      OTHERS      = 3.\n'
                                                                                              '  IF sy-subrc <> 0.\n'
                                                                                              '    MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno\n'
                                                                                              '            WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.\n'
                                                                                              '  ENDIF.\n\n')

    def get_ddic_type(self):
        # type: (str) -> str

        try:
            val = self.ddic[self.data_type]
        except KeyError:
            val = self.var_name
        return val

# class DataDescription:
#     def __init__(self):

# Valores possiveis apra data_type:
#   STRG    String
#   NUMC    String de Numeros
#   DEC     Valor Decimal
#   ACCP    Periodo YYYY-MM
#   DATS    Data    YYYY-MM-DD
