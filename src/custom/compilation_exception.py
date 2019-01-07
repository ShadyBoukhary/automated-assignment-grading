class CompilationException(Exception):
    '''Raise when a specific subset of values in context of app is wrong'''
    def __init__(self, message, foo, *args):
        self.message = message 
        # Special attribute you desire with your Error, 
        # perhaps the value that caused the error?:
        self.foo = foo         
        # allow users initialize misc. arguments as any other builtin Error
        super(CompilationException, self).__init__(message, foo, *args) 