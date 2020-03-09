class AssignmentException(Exception):
    def __init__(self, message, details='', *args):
        self.message = message
        self.details = details
        super(AssignmentException, self).__init__(message, details, *args)
