import xml.etree.ElementTree as ET
from xmlElement import XmlElement as XmlElement


class XsdDocument:
    def __init__(self, file_name):
        self.doc_tree = ET.parse(file_name)

    def get_root_node(self):
        # type: () -> XmlElement
        return XmlElement(self.doc_tree.getroot())
