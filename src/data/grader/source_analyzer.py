from core.assignment import Assignment
from core.individual_assignment import IndividualAssignment
from custom.compilation_exception import CompilationException
from utils.utilities import Utilities


def analyze_source(path, assignment, individual_assignment):
    try:
        result, error = verify_compilation(path, individual_assignment.get_compile_output_dir(), individual_assignment.get_compile_output_path(), "cpp")
        if result:
            source = Utilities.read_file(path)
            # TODO: Keep track of functions in source, maybe loops too?
            print("Compiles!")
        else:
            raise CompilationException("Source code does not compile!", error)
    except IOError as e:
        print(e)


def verify_compilation(path, compile_output_dir, compile_output_path, language):
    """Checks whether a source code for an assignment compiles
    
    Args:
        path (String): path of the source code
        compile_output_dir (String): Output directory of the compilation result
        compile_output_path (String): Output path of the compilation result file
        language (String): Programming language to be compiled

    Returns:
        (boolean, String): Tuple with a flag indicating compilation result and any error messages
    
    """

    Utilities.compile_source(path, compile_output_dir, compile_output_path, language)
    compile_results = Utilities.read_file(compile_output_path)
    Utilities.delete_file(compile_output_path)

    if len(compile_results) < 1:
        return True, None
    return False, compile_results
