class XmlElement:
    def __init__(self, xml_element):
        self.node = xml_element

    def get_attributes(self):
        # type: () -> dict
        return self.node.attrib

    def get_attribute_by_name(self, attr_name):
        # type: (str) -> str
        try:
            return self.node.attrib[attr_name]
        except KeyError:
            return ''

    def get_qualified_name(self):
        # type: () -> str
        return self.node.tag

    def get_tag_name(self):
        # type: () -> str
        return self.node.tag.split('}')[1]

    def get_tag_namespace(self):
        # type: () -> str
        namespace = self.node.tag.split('}')[0]
        return namespace.replace('{', '')

    def get_children_nodes(self):
        # type: () -> [XmlElement]
        return [XmlElement(a) for a in list(self.node)]

    def get_value(self):
        # type: () -> str
        return self.node.text
