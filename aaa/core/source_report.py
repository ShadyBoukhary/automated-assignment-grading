from aaa.core.function import Function
import copy
from pprint import pprint
import json


class SourceReport(dict):

    def __init__(self, functions=[]):
        self.functions = functions

    def addFunction(self, function):
        if not self.functions.__contains__(function):
            self.functions.append(function)

    @classmethod
    def from_json(cls, data):
        functions = data["functions"]
        if functions is None:
            return cls([])
        else:
            sr = cls(data["functions"])
            sr.functions = list(map(Function.from_json, data["functions"]))
            return sr

    def to_dict(self):
        dic = copy.deepcopy(self.__dict__)
        dic["functions"] = [fun.to_dict() for fun in self.functions]

        return dic
