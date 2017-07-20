from abc import abstractmethod


class AbapCommand:
    def __init__(self):
        self.command = list()

    def _add_command(self, text):
        # type: (str) -> ()

        if not text.endswith('\n'):
            text += '\n'
        self.command.append(text)

    @abstractmethod
    def build_command(self):
        return
