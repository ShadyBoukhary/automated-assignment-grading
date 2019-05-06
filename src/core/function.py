class Function:
    def __init__(self, name, return_type, arguments):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments

    def __eq__(self, other):
        if isinstance(other, Function):
            return self.name == other.name and self.return_type == other.return_type and self.arguments == other.arguments
        return NotImplemented
        
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result