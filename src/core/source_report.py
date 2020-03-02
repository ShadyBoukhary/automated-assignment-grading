from core.function import Function
import copy


class SourceReport(dict):

    def __init__(self, primitive_types=[], functions=[]):
        self.primitive_types = primitive_types
        self.functions = functions

    def addFunction(self, function):
        if not self.functions.__contains__(function):
            self.functions.append(function)

    @classmethod
    def from_json(cls, data):
        sr = cls(data["primitive_types"], data["functions"])
        sr.functions = list(map(Function.from_json, data["functions"]))

    def to_dict(self):
        dic = copy.deepcopy(self.__dict__)
        dic["functions"] = [fun.to_dict() for fun in self.functions]

        return dic
