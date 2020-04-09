class CompilationException(Exception):
    def __init__(self, message, details, *args):
        self.message = message
        self.details = details
        super(CompilationException, self).__init__(message, details, *args)
