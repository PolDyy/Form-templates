
class NameFileException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class R1Exception(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EmptyDirException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message
