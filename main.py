import re
import rstr

from xsdDocument import XsdDocument
from xmlElement import XmlElement
from DataStructure import DataStructure


def generate_data_structure(xsd_doc):
    # type: (XsdDocument) -> Optional[DataStructure]

    root_node = xsd_doc.get_root_node()

    if not root_node_is_valid(root_node):
        return None

    print get_event_info(root_node)

    children_nodes = root_node.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name
        if tag() == 'element':
            ds = parse_element(node, None)
        elif tag() == 'complexType':
            ds.append_child(parse_complex_type(node, None))
        else:
            print 'tag ' + tag() + " nao tratada"

    return ds


def parse_element(element, parent):
    # type: (XmlElement,DataStructure) -> DataStructure

    ds = DataStructure()
    ds.xml_name = element.get_attribute_by_name('name')
    if ds.xml_name == '':
        ds.xml_name = element.get_attribute_by_name('ref')
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
        ds.xml_name = element.get_attribute_by_name('name')

    ds.xml_type = 'S'

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

    attr_ds.xml_type = 'A'
    attr_ds.xml_name = element.get_attribute_by_name('name')
    if element.get_attribute_by_name('use') == 'required':
        attr_ds.min_occurs = 1
        attr_ds.max_occurs = 1

    ds.append_child(attr_ds)

    children_nodes = element.get_children_nodes()

    for node in children_nodes:
        tag = node.get_tag_name()
        if tag == 'simpleType':
            parse_simple_type(attr_ds)
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


def parse_simple_type(element, ds):
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
    if base == 'string':
        return 'STRG'
    elif base == 'byte' or 'unsignedInt' or 'integer':
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

    for i in range(0, 1000):
        x = rstr.xeger(ds.pattern)
        length.add(len(x))

    ds.max_length = max(length)
    ds.min_length = min(length)

    if ds.min_length == 7 and ds.max_length == 7 and x[4] == '-':
        ds.data_type = 'ACCP'

    if re.match('\d+,\d{2,}',x):
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
    if not re.match('http://www.reinf.esocial.gov.br/schemas/\w+/v\d{2}_\d{2}_\d{2}', namespace):
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
        return int(value)


def main():
    xsd = XsdDocument('XSD/1.0/evtInfoContri.xsd')

    l = set()

    # ds = generate_data_structure(xsd)


if __name__ == '__main__':
    main()