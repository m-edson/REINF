from abapHelper import *
from abap.abapTypes import *


def create(obj):
    return obj.build()


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


def _init_ddic():
    ddic = dict()
    ddic['ACCP'] = 'Z_REINF_PERIODO'

    ddic['STRG'] = 'Z_REINF_TEXTO'
    ddic['xs:ID'] = 'Z_REINF_TEXTO'

    ddic['NUMC'] = 'Z_REINF_NUMERO'

    ddic['DEC'] = 'Z_REINF_VALOR'

    ddic['DATS'] = 'Z_REINF_DATA'

    return ddic


class DataStructure:
    ddic = _init_ddic()

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

    def __repr__(self):
        if self._children:
            r = '(' + str(self.var_name)
            for c in self._children:
                r += repr(c)
            r += ')'
            return r
        else:
            return '(' + str(self.var_name) + ',' + str(self.data_type) + ',' + str(self.min_occurs) + ',' + str(
                self.max_occurs) + ',' + str(self.min_length) + ',' + str(self.max_length) + ',' + str(
                self.pattern) + ')'

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

    def write_ddic_generator(self, write=True, command_stack=[]):
        # type: (bool,list) -> ()

        if self.var_name == 'REINF':
            self.get_children_nodes()[0].write_ddic_generator(False, command_stack)
        else:

            if self.xml_type == 'G':
                if self.max_occurs > 1:
                    tab_cat_name = self.var_name + '_T'
                    command_stack.append(AbapHelper.cat_tab_activate(tab_cat_name))
                    command_stack.append(AbapHelper.cat_tab_put(tab_cat_name))
                    command_stack.append(AbapHelper.cat_tab_info(tab_cat_name, self.var_name, 'PYGEN'))

                command_stack.append(AbapHelper.tabl_activate(self.var_name))
                command_stack.append(AbapHelper.tabl_put(self.var_name))
                command_stack.append(AbapHelper.struct_def(self.var_name, 'PYGEN'))

                count = 1
                for n in self.get_children_nodes():
                    if n.max_occurs > 1:
                        tab_cat_name = n.var_name + '_T'
                        command_stack.append(AbapHelper.struct_line(self.var_name, n.var_name, tab_cat_name, count))
                    else:
                        command_stack.append(
                            AbapHelper.struct_line(self.var_name, n.var_name, n.get_ddic_type(), count))
                    count += 1
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

    def write_method_file(self, f=None, level=-1, obj_repr=[]):
        # type: (file, int) -> str
        s = []
        if level == -1:
            path = 'output/' + self.name + '_' + self.version + '.abap'
            f = open(path, 'w')

            s.append('METHOD create_out_format.\n')
            s.append('DATA: lw_out_format TYPE zsoutputformat.\n\n')

            s.append('DEFINE monta_formatador_1.\n\n')

            s.append('lw_out_format-level = &1.\n')
            s.append('lw_out_format-var_name = &2.\n')
            s.append('lw_out_format-xml_name = &3.\n')
            s.append('lw_out_format-xml_type = &4.\n')
            s.append('lw_out_format-min_occurs = &5.\n')
            s.append('lw_out_format-max_occurs = &6.\n')
            s.append('lw_out_format-min_length = &7.\n')
            s.append('lw_out_format-max_length = &8.\n')
            s.append('lw_out_format-pattern = &9.\n\n')

            s.append('END-OF-DEFINITION.\n\n')

            s.append('DEFINE monta_formatador_2.\n\n')
            s.append('lw_out_format-datatype = &1.\n')
            s.append('APPEND lw_out_format TO ct_out_format.\n')
            s.append('CLEAR lw_out_format.\n\n')
            s.append('END-OF-DEFINITION.\n\n')

        if not obj_repr.__contains__(repr(self)):
            s.append('monta_formatador_1 ' + str(level) + ' \'' + str(self.var_name) + '\'' + ' \'' + str(
                self.xml_name) + '\'' + ' \'' + str(self.xml_type) + '\' ' + str(self.min_occurs) + ' ' + str(
                self.max_occurs) + ' ' + str(self.min_length) + ' ' + str(self.max_length) + ' ' + '\'' + str(
                self.pattern) + '\'' + '.\n')
            s.append('monta_formatador_2 ' + '\'' + str(self.data_type) + '\'' + '.\n\n')
            obj_repr.append(repr(self))

        for child in self._children:
            s += child.write_method_file(f, level + 1, obj_repr)

        if level == -1:
            s.append('ENDMETHOD.\n')
            for command in s:
                f.write(command)
            f.close()
        return s

    def get_ddic_type(self):
        # type: (str) -> str

        try:
            val = self.ddic[self.data_type]
        except KeyError:
            val = self.var_name
        return val

    def gen_local_types(self, write=True, command_stack=[], obj_list=[]):
        # type: (bool,list) -> ()

        if self.var_name == 'REINF':
            self.get_children_nodes()[0].gen_local_types(False, command_stack)
        else:
            types = AbapTypesBuilder()
            if self.xml_type == 'G':

                if self.max_occurs > 1:
                    obj_list.append(create(AbapTypesBuilder()
                                           .cretate_types()
                                           .add_declaration(AbapDeclarationBuilder()
                                                            .set_name(self.var_name + '_T')
                                                            .set_type(self.var_name)
                                                            .set_ttype().type_table_of()
                                                            .build())))
                    #
                    #     command_stack.append(AbapHelper.local_table_type(self.var_name))
                    #
                    # command_stack.append(AbapHelper.local_types_end(self.var_name))
                types.create_types_begin_of(self.var_name)

                for n in self.get_children_nodes():
                    if n.max_occurs > 1:
                        tab_cat_name = n.var_name + '_T'
                        types.add_declaration(AbapDeclarationBuilder()
                                              .set_name(n.var_name)
                                              .set_type(tab_cat_name)
                                              .build())

                        # command_stack.append(AbapHelper.local_types_line(n.var_name, tab_cat_name))
                    else:
                        types.add_declaration(AbapDeclarationBuilder()
                                              .set_name(n.var_name)
                                              .set_type(n.get_ddic_type())
                                              .build())
                        # command_stack.append(AbapHelper.local_types_line(n.var_name, n.get_ddic_type()))
                        # command_stack.append(abap_types.build_command())
                        # decl_strct.add(repr(self))
                obj_list.append(types.build())

            for n in self.get_children_nodes():
                n.gen_local_types(False, command_stack, obj_list)

        objects = []
        if write is True:
            f = open('output/locl_' + self.name + '-' + self.version + '.abap', 'w')
            printed_commands = list()
            while obj_list:
                obj = obj_list.pop()
                if not printed_commands.__contains__(str(obj)):
                    f.write(str(obj))
                    objects.append(obj)
                    printed_commands.append(str(obj))
            f.close()
        return objects


def _uniquify(l):
    # type: (list) -> list
    unique = []
    for item in l:
        if item not in unique:
            unique.append(item)
    return unique

# class DataDescription:
#     def __init__(self):

# Valores possiveis apra data_type:
#   STRG    String
#   NUMC    String de Numeros
#   DEC     Valor Decimal
#   ACCP    Periodo YYYY-MM
#   DATS    Data    YYYY-MM-DD
