class CompilationException(Exception):
    def __init__(self, message, details, *args):
        self.message = message 
        # Special attribute you desire with your Error, 
        # perhaps the value that caused the error?:
        self.details = details         
        # allow users initialize misc. arguments as any other builtin Error
        super(CompilationException, self).__init__(message, details, *args) 