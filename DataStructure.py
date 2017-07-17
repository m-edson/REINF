class DataStructure:
    def __init__(self):
        self._children = []
        self._parent = None
        self.name = ''
        self.version = ''
        self._types = []

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

    def write_ddic_generator(self):
        pass

    def resolve_type_references(self, types, type_names=None):
        # type: () -> ()

        if type_names is None:
            type_names = [x.xml_name for x in types]

        for node in self._children:
            if type_names.__contains__(node.data_type):
                node._children = types[type_names.index(node.data_type)]._children
                node.data_type = ''
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

        # f.write('lw_out_format-level = ' + str(level) + '\n')
        # f.write('lw_out_format-var_name = ' + '\'' + str(self.var_name) + '\'' + '\n')
        # f.write('lw_out_format-xml_name = ' + '\'' + str(self.xml_name) + '\'' + '\n')
        # f.write('lw_out_format-xml_type = ' + '\'' + str(self.xml_type) + '\'' + '\n')
        # f.write('lw_out_format-min_occurs = ' + str(self.min_occurs) + '\n')
        # f.write('lw_out_format-max_occurs = ' + str(self.max_occurs) + '\n')
        # f.write('lw_out_format-min_length = ' + str(self.min_length) + '\n')
        # f.write('lw_out_format-max_length = ' + str(self.max_length) + '\n')
        # f.write('lw_out_format-pattern = ' + '\'' + str(self.pattern) + '\'' + '\n')
        # f.write('lw_out_format-datatype = ' + '\'' + str(self.data_type) + '\'' + '\n')
        # f.write('APPEND lw_out_format TO ct_out_format.\n')
        # f.write('CLEAR lw_out_format.\n\n')

        for child in self._children:
            child.write_method_file(f, level + 1)

        if level == -1:
            f.write('ENDMETHOD.\n')

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

        if self.data_type == 'ACCP':
            return 'Z_REINF_PERIODO'
        elif self.data_type == 'STRG':
            return 'Z_REINF_TEXTO'
        elif self.data_type == 'NUMC':
            return 'Z_REINF_NUMERO'
        elif self.data_type == 'DEC':
            return 'Z_REINF_VALOR'
        elif self.data_type == 'DATS':
            return 'Z_REINF_DATA'
        else:
            return '?'

#
# class DataDescription:
#     def __init__(self):

# Valores possiveis apra data_type:
#   STRG    String
#   NUMC    String de Numeros
#   DEC     Valor Decimal
#   ACCP    Periodo YYYY-MM
#   DATS    Data    YYYY-MM-DD
