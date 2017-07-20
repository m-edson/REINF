class AbapTypes:
    def __init__(self, name=''):
        # type: (str) -> AbapTypes
        self._name = name
        self._types = []

    def add_type(self, name, type):
        # type: (str,str) -> ()
        self._types.append((name, type))

    def build_command(self):
        if self._name == '' and len(self._name) == 1:
            t = self._types[0]
            return ['TYPES ' + t[0] + '_T TYPE TABLE OF ' + t[0] + ' WITH NON-UNIQUE DEFAULT KEY.']
        else:
            if self._types:
                commands = list()
            commands.append('TYPES: BEGIN OF ' + self._name + ',')
            for t in self._types:
                commands.append(t[0] + ' TYPE ' + t[1] + ',')
            commands.append('END OF ' + self._name + '.')
            return commands
