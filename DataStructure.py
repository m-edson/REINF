class DataStructure:
    def __init__(self):
        self._children = []
        self._parent = None

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

    def append_child(self, ds):
        # type: (DataStructure) -> ()
        self._children.append(ds)
        ds._parent = self

    def get_parent(self):
        # type: () -> DataStructure
        return self._parent

#
# class DataDescription:
#     def __init__(self):

# Valores possiveis apra data_type:
#   STRG    String
#   NUMC    String de Numeros
#   DEC     Valor Decimal
#   ACCP    Periodo YYYY-MM
#   DATS    Data    YYYY-MM-DD
#   STRUCT  Estrutura
