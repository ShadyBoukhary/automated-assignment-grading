from core.function import Function

class SourceReport(dict):

    def __init__(self, primitive_types):
        self.primitive_types = primitive_types
        self.functions = []

    def addFunction(self, function):
        if not self.functions.__contains__(function):
            self.functions.append(function)

    @classmethod
    def from_json(cls, data):
        sr = cls(**data)
        sr.functions = list(map(Function.from_json, data["functions"]))


    def to_dict(self):
        dic = self.__dict__
        dic["functions"] = [fun.to_dict() for fun in self.functions]
        return dic