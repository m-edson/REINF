# coding=utf-8
import re
import sys

import rstr

from os import listdir
from os.path import isfile, join

from DataStructure import DataStructure
from xmlElement import XmlElement
from xsdDocument import XsdDocument

from abap.abapClass import *

special_characters = ['\\', '^', '$', '.', '|', '?', '*', '+', '(', ')', '[', ']', '{', '}']


def generate_data_structure(xsd_doc):
    # type: (XsdDocument) -> ((str,str), DataStructure)

    root_node = xsd_doc.get_root_node()

    if not root_node_is_valid(root_node):
        return None

    info = get_event_info(root_node)

    children_nodes = root_node.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name
        if tag() == 'element':
            ds = parse_element(node, None)
        elif tag() == 'complexType':
            ds.append_type_ref(parse_complex_type(node, None))
        else:
            print 'tag <' + tag() + '/> nao tratada'

    ds.name = info[0]
    ds.version = info[1]

    ds.resolve_type_references(ds.get_types())

    return ds, info


def parse_element(element, parent):
    # type: (XmlElement,DataStructure) -> DataStructure

    ds = DataStructure()
    ds.xml_node = element
    ds.xml_name = element.get_attribute_by_name('name')
    if ds.xml_name == '':
        ds.xml_name = element.get_attribute_by_name('ref')
    ds.var_name = camel_case_to_underscore(ds.xml_name)
    ds.min_occurs = get_occurs(element.get_attribute_by_name('minOccurs'))
    ds.max_occurs = get_occurs(element.get_attribute_by_name('maxOccurs'))
    ds.data_type = element.get_attribute_by_name('type')

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'complexType':
            parse_complex_type(node, ds)
        elif tag == 'simpleType':
            parse_simple_type(node, ds)
        elif tag == 'annotation':
            parse_annotation(node, ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'

    if parent is None:
        return ds
    else:
        parent.append_child(ds)
        return parent


def parse_annotation(element, ds):
    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'documentation':
            ds.documentation = node.get_value()
        else:
            print 'Tag <' + tag + '/> nao tratada'


def parse_complex_type(element, ds):
    if ds is None:
        ds = DataStructure()
        ds.xml_node = element
        ds.xml_name = element.get_attribute_by_name('name')
        ds.var_name = camel_case_to_underscore(ds.xml_name)

    ds.xml_type = 'G'

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'sequence':
            parse_sequence(node, ds)
        elif tag == 'attribute':
            parse_attribute(node, ds)
        elif tag == 'annotation':
            parse_annotation(node, ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'

    return ds


def parse_attribute(element, ds):
    attr_ds = DataStructure()

    attr_ds.xml_node = element
    attr_ds.xml_type = 'A'
    attr_ds.xml_name = element.get_attribute_by_name('name')
    attr_ds.var_name = camel_case_to_underscore(attr_ds.xml_name)
    attr_ds.data_type = element.get_attribute_by_name('type')
    ds.var_name = camel_case_to_underscore(ds.xml_name)
    if element.get_attribute_by_name('use') == 'required':
        attr_ds.min_occurs = 1
        attr_ds.max_occurs = 1

    ds.append_child(attr_ds)

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'simpleType':
            parse_simple_type(node, attr_ds, True)
        elif tag == 'annotation':
            parse_annotation(node, attr_ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'


def parse_sequence(element, ds):
    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'element':
            parse_element(node, ds)
        elif tag == 'choice':
            parse_sequence(node, ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'


def parse_union(element, ds):
    # type: (XmlElement,DataStructure) -> ()
    children_nodes = element.get_children_nodes()

    types = []

    for node in children_nodes:
        tag = node.get_tag_name()
        ds_aux = DataStructure()
        if tag == 'simpleType':
            parse_simple_type(node, ds_aux)
            verify_pattern(ds_aux)
            types.append(ds_aux)
        else:
            print 'Tag <' + tag + '/> nao tratada'

    ds.max_length = 0
    ds.min_length = 99999999
    ds.pattern = ''
    ds.data_type = 'STRG'
    for t in types:
        if ds.max_length < t.max_length:
            ds.max_length = t.max_length
        if ds.min_length > t.min_length:
            ds.min_length = t.min_length
        if ds.pattern == '':
            ds.pattern += t.pattern
        else:
            ds.pattern += '|' + t.pattern


def parse_simple_type(element, ds, attribute=False):
    if attribute is False:
        ds.xml_type = 'E'

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'restriction':
            parse_restriction(node, ds)
        elif tag == 'union':
            parse_union(node, ds)
        elif tag == 'annotation':
            parse_annotation(node, ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'


def get_data_type(base_attr):
    # type: (str) -> str
    base = base_attr.split(':')[1]
    if base == 'string' or base == 'ID':
        return 'STRG'
    elif base == 'byte' or base == 'unsignedInt' or base == 'integer' or base == 'unsignedByte' or base == 'unsignedLong':
        return 'NUMC'
    elif base == 'decimal':
        return 'DEC'
    elif base == 'gYearMonth':
        return 'ACCP'
    elif base == 'date':
        return 'DATS'
    else:
        return '?'


def verify_pattern(ds):
    # type: (DataStructure) -> ()

    length = set()
    x = None

    for i in range(0, 1000):
        x = rstr.xeger(ds.pattern)
        length.add(len(x))

    ds.max_length = max(length)
    ds.min_length = min(length)

    if ds.min_length == 7 and ds.max_length == 7 and x[4] == '-':
        ds.data_type = 'ACCP'

    if re.match('\d+,\d{2,}', x):
        ds.data_type = 'DEC'


def parse_restriction(element, ds):
    # type: (XmlElement, DataStructure) -> ()
    ds.data_type = get_data_type(element.get_attribute_by_name('base'))

    if ds.data_type == 'DATS':
        ds.min_length = 10.
        ds.max_length = 10.

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'minLength':
            ds.min_length = int(node.get_attribute_by_name('value'))
        elif tag == 'maxLength':
            ds.max_length = int(node.get_attribute_by_name('value'))
        elif tag == 'pattern':
            ds.pattern = node.get_attribute_by_name('value')
            verify_pattern(ds)
        elif tag == 'length':
            ds.min_length = int(node.get_attribute_by_name('value'))
            ds.max_length = int(node.get_attribute_by_name('value'))
        elif tag == 'enumeration':
            for ch in special_characters:
                pattern = node.get_attribute_by_name('value').replace(ch, '\\' + ch)
            if ds.pattern == '':
                ds.pattern += pattern
            else:
                ds.pattern += '|' + pattern
        elif tag == 'minInclusive':
            ds.min_value = int(node.get_attribute_by_name('value'))
        elif tag == 'maxInclusive':
            ds.max_value = int(node.get_attribute_by_name('value'))
        elif tag == 'totalDigits':
            ds.max_length = int(node.get_attribute_by_name('value'))
        elif tag == 'fractionDigits':
            ds.decimals = int(node.get_attribute_by_name('value'))
        elif tag == 'whiteSpace':
            ds.whitespace = node.get_attribute_by_name('value')

        else:
            print 'Tag <' + tag + '/> nao tratada'


def root_node_is_valid(node):
    # type: (XmlElement) -> bool

    node_is_valid = True

    if node.get_tag_name() != 'schema':
        node_is_valid = False

    namespace = node.get_attribute_by_name('targetNamespace')
    if not re.match('http://www.reinf.esocial.gov.br/schemas/\w+/v\d{1,2}_\d{2}_\d{2}', namespace):
        node_is_valid = False

    return node_is_valid


def get_event_info(root_node):
    # type: (XmlElement) -> (str,str)

    namespace = root_node.get_attribute_by_name('targetNamespace')

    namespace = namespace.replace('http://www.reinf.esocial.gov.br/schemas/', '')
    info = namespace.split('/')

    event_name = info[0]
    event_version = info[1]
    event_version = event_version.replace('v', '')

    return event_name, event_version


def get_occurs(value):
    if value == '':
        return 1
    else:
        try:
            return int(value)
        except ValueError:
            if value == 'unbounded':
                return sys.maxint
            else:
                raise ValueError('Valor nao esperado: %s' % value)


def underscore_to_camel_case(text):
    # type: (str) -> str
    tokens = text.split('_')
    result = [tokens[0].lower()]
    result += map(str.title, tokens[1:])
    return ''.join(result)


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


def create(obj):
    return obj.build()


def generate_class(namespace, version, types, method_code):
    # type: (str,[AbapTypes],[str]) -> AbapClass

    class_name = file_name_to_class_name('CL_', namespace, version)
    f = open('output/' + version + '/' + class_name + '.abap', 'w')

    private_section_builder = AbapClassSectionBuilder().create_private_session()
    for tp in types:
        private_section_builder.add_declaration(tp)

    private_section_builder.add_declaration(AbapDeclarationBuilder()
                                            .set_name('event_data')
                                            .set_type(types[-1].name)
                                            .build())
    private_section = private_section_builder.build()

    AbapClassSectionBuilder().create_protected_session()

    protected_section = create(AbapClassSectionBuilder()
                               .create_protected_session()
                               .add_method(AbapClassMethodBuilder()
                                           .set_method_name('build')
                                           .set_redefinition()
                                           .add_code(build_method_type_check_code())
                                           .build())
                               .add_method(AbapClassMethodBuilder()
                                           .set_method_name('set_xml_descr')
                                           .set_redefinition()
                                           .add_code(method_code).build())
                               .add_method(AbapClassMethodBuilder()
                                           .set_method_name('get_root_node_name')
                                           .set_redefinition()
                                           .add_code(
        ['rv_node_name = \'' + underscore_to_camel_case(types[-1].name) + '\'.'])
                                           .build())
                               .add_method(AbapClassMethodBuilder()
                                           .set_method_name('get_namespace')
                                           .set_redefinition()
                                           .add_code(['rv_namespace = \'' + namespace + '\'.'])
                                           .build())
                               .add_method(AbapClassMethodBuilder()
                                           .set_method_name('get_version')
                                           .set_redefinition()
                                           .add_code(['rv_version = \'' + version + '\'.'])
                                           .build()))

    public_section = create(AbapClassSectionBuilder()
                            .create_public_session()
                            .add_method(AbapClassMethodBuilder()
                                        .set_method_name('get_xml_data')
                                        .set_redefinition()
                                        .add_code(['GET REFERENCE OF me->event_data INTO ro_xml_data.'])
                                        .build()))

    cls = create(AbapClassBuilder()
                 .set_class_name('/VTAX/' + class_name)
                 .set_parent_class('/VTAX/CL_REINF_EVENT_XML')
                 .set_final()
                 .set_private_session(private_section)
                 .set_protected_session(protected_section)
                 .set_public_session(public_section))

    f.write(str(cls))
    f.close()
    return cls


class_name_map = dict()


def init_class_name_dict():
    class_name_map['evtInfoContribuinte'] = 'R1000'
    class_name_map['evtEspDesportivo'] = 'R3010'
    class_name_map['evtExclusao'] = 'R9000'
    class_name_map['evtFechamento'] = 'R2099'
    class_name_map['evtInfoCPRB'] = 'R2060'
    class_name_map['evtInfoProdRural'] = 'R2050'
    class_name_map['evtPgtosDivs'] = 'R2070'
    class_name_map['evtPrestadorServicos'] = 'R2020'
    class_name_map['evtReabreEvPer'] = 'R2098'
    class_name_map['evtRecursoRecebidoAssociacao'] = 'R2030'
    class_name_map['evtRecursoRepassadoAssociacao'] = 'R2040'
    class_name_map['evtTabProcesso'] = 'R1070'
    class_name_map['evtTomadorServicos'] = 'R2010'
    class_name_map['retornoTotalizadorContribuinte'] = 'R5001'
    class_name_map['retornoEvento'] = 'RetEvt'
    class_name_map['retornoLoteEventos'] = 'RetLoteEvts'


def file_name_to_class_name(prefix, evt_name, version):
    # type: (str,str,str) -> str
    class_name = prefix + class_name_map[evt_name]
    class_name += '_XML_' + version
    return class_name


def build_method_type_check_code():
    code = []
    code.append('DATA: lo_type_descr  TYPE REF TO cl_abap_typedescr,\n')
    code.append('      lo_class_descr TYPE REF TO cl_abap_classdescr,\n')
    code.append('      lo_r1000     TYPE REF TO /VTAX/CL_R1000,\n')
    code.append('  class_type     TYPE string.\n')

    code.append('\nlo_type_descr = cl_abap_typedescr=>describe_by_object_ref( p_object_ref = evt_data ).\n')

    code.append('\nTRY.\n')
    code.append('    lo_class_descr ?= lo_type_descr.\n')
    code.append('  CATCH cx_sy_move_cast_error.\n')
    code.append('    MESSAGE \'Tipo do parâmetro incorreto. Era esperado um objeto.\' TYPE \'E\'.\n')
    code.append('ENDTRY.\n')

    code.append('class_type = lo_class_descr->get_relative_name( ).\n')
    code.append('TRY.\n')
    code.append('    lo_r1000 ?= evt_data.\n')
    code.append('  CATCH cx_sy_move_cast_error.\n')
    code.append('    MESSAGE \'Classe incorreta\' TYPE \'E\'.\n')
    code.append('ENDTRY.\n')
    code.append('****************************************\n')
    code.append('*************YOUR CODE HERE*************\n')
    code.append('****************************************\n')
    return code


def generate_field_descr_file(data_structure, evt_name, version, field_descr_set=None):
    # type: (DataStructure,str,str,set) -> None

    first_iter = False
    if field_descr_set is None:
        file_name = class_name_map[evt_name] + '_field_drescr'
        file_obj = open('output/' + version + '/' + file_name + '.csv', 'w')
        first_iter = True
        field_descr_set = set()

    if data_structure.xml_type == 'A' or data_structure.xml_type == 'E':
        file_line = version + ';' + class_name_map[evt_name] + ';' \
                    + data_structure.xml_name + ';' \
                    + data_structure.var_name + ';' \
                    + data_structure.documentation + '\n'
        file_line = file_line.encode('cp1252')
        file_line = ' '.join(file_line.split())
        file_line.replace('\n', ' ')
        file_line = file_line.lstrip()
        file_line = file_line.rstrip()
        field_descr_set.add(file_line)
    else:
        for ds in data_structure.get_children_nodes():
            generate_field_descr_file(ds, evt_name, version, field_descr_set)

    if first_iter is True:
        for s in field_descr_set:
            file_obj.write(s)
            file_obj.write('\n')


def main():
    init_class_name_dict()

    path = 'XSD/nfse/'
    files = [path + f for f in listdir(path) if isfile(join(path, f))][:-1]

    for f in files:
        # xsd = XsdDocument('XSD/1.1.01/evtTabProcesso-v1_01_01.xsd')
        xsd = XsdDocument(f)

        ds, info = generate_data_structure(xsd)

        evt_name, version = info

        method = ds.write_method_file()[1:-1]

        obj_list = ds.gen_local_types()

        cls = generate_class(evt_name, version, obj_list, method)

        generate_field_descr_file(ds, evt_name, version)


def main2():
    pass


if __name__ == '__main__':
    # main2()
    main()
