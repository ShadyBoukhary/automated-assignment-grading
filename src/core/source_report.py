class SourceReport:

    def __init__(self, primitive_types):
        self.primitive_types = primitive_types
        self.functions = []

    def addFunction(self, function):
        if not self.functions.__contains__(function):
            self.functions.append(function)