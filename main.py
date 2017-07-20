# coding=utf-8
import re
import sys

import rstr

from DataStructure import DataStructure
from xmlElement import XmlElement
from xsdDocument import XsdDocument


def generate_data_structure(xsd_doc):
    # type: (XsdDocument) -> Optional[DataStructure]

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
            print 'tag ' + tag() + " nao tratada"

    ds.name = info[0]
    ds.version = info[1]

    ds.resolve_type_references(ds.get_types())

    return ds


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
        else:
            print 'Tag <' + tag + '/> nao tratada'

    if parent is None:
        return ds
    else:
        parent.append_child(ds)
        return parent


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


def parse_simple_type(element, ds, attribute=False):
    if attribute is False:
        ds.xml_type = 'E'

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'restriction':
            parse_restriction(node, ds)
        else:
            print 'Tag <' + tag + '/> nao tratada'


def get_data_type(base_attr):
    # type: (str) -> str
    base = base_attr.split(':')[1]
    if base == 'string' or base == 'ID':
        return 'STRG'
    elif base == 'byte' or base == 'unsignedInt' or base == 'integer':
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
    ds.data_type = get_data_type(element.get_attribute_by_name('base'))

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


def main():
    # xsd = XsdDocument('XSD/1.0/evtInfoContri.xsd')
    xsd = XsdDocument('XSD/1.1.01/evtInfoContribuinte-v1_01_01.xsd')

    ds = generate_data_structure(xsd)

    ds.write_method_file()

    # ds.write_ddic_generator()

    ds.gen_local_types()


def main2():
    from zeep import Client
    from zeep.wsse.signature import Signature

    client = Client('https://preprodefdreinf.receita.fazenda.gov.br/RecepcaoLoteReinf.svc', wsse=Signature(
        'C:\Users\SEIDOR\AppData\Roaming\Skype\My Skype Received Files\certidao.pfx',
        'C:\Users\SEIDOR\AppData\Roaming\Skype\My Skype Received Files\certidao.pfx',
        '12345678'))
    # client.service.RecepcaoLoteReinf()
    # result = client.service.ConvertSpeed(
    #     100, 'kilometersPerhour', 'milesPerhour')

    # print result
    #
    # assert result == 62.137

if __name__ == '__main__':
    # main()
    main2()
