class Function:
    def __init__(self, name, return_type, arguments):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.__dict__
        
    def __eq__(self, other):
        if isinstance(other, Function):
            return self.name == other.name and self.return_type == other.return_type and self.arguments == other.arguments
        return NotImplemented
        
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result