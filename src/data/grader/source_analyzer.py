from core.assignment import Assignment
from core.function import Function
from core.individual_assignment import IndividualAssignment
from core.source_report import SourceReport
from custom.compilation_exception import CompilationException
from utils.constants import Constants
from utils.utilities import Utilities


def analyze_source(path, assignment, individual_assignment):
    """Analyzes a source file. 
    
    Checks if the source file compiles, compiles it, finds all functions present in the source file and gathers their signiture.
    If the file does not compile, a CompilationException is raised.

    Args:
        path (String): the path of the source file
        assignment (Assignment): the course assignment being graded.
        individual_assignment (IndividualAssignment): the student assignment being evaluated and analyzed

    Returns: 
        (SourceReport): the report about the source containing function information

    Raises:
        (CompilationException): if the source file does not compile
    
    """

    Utilities.log("Compiling... ", True)
    Utilities.flush()
    try:
        result, error = verify_compilation(path, individual_assignment.get_compile_output_dir(), individual_assignment.get_compile_output_path(), "cpp", individual_assignment)
        if result:
            source = Utilities.read_file(path)
            # TODO: Keep track of functions in source, maybe loops too?
            source_report = analyze(source, "cpp")
            Utilities.log(Constants.CHECK_MARK)
            return source_report
        else:
            raise CompilationException(Constants.CROSS_MARK, error)
    except IOError as e:
        Utilities.log(e)


def analyze(source, language):
    source = clean_source(source)

    if language == "cpp":
        return analyze_cpp(source)


def analyze_cpp(source):
    """Analyzes a C++ source file

    Finds all function declaration and generates a report based on the functions found.
    
    Args:
        source (String): contents of the source file

    Returns:
        SourceReport: the report generated using the given source file contents
    
     """
    source_report = SourceReport(Constants.CPP_PRIMITIVE_TYPES)
    # get lines starting with a primitive type
    lines_with_types = get_lines_starting_with_types(source)
    # filter by lines containing "(" indicating a function, clean the string containing the function
    lines_with_types = [clean_function_line(line) for line in lines_with_types if line.__contains__("(")]
    # remove main function from list
    lines_with_types = [line for line in lines_with_types if not line == "int main"]
    # generate list of functions (every line is in the format: return_type name arg1 arg2 arg3 ....)
    functions = [Function(line.split()[1], line.split()[0], get_arguments(line)) for line in lines_with_types]
    # add functions to report, duplicate ones such as prototypes and definitions are not duplicated
    for f in functions:
        source_report.addFunction(f)

    return source_report


def get_lines_starting_with_types(source):
    return [line for line in source if Constants.CPP_PRIMITIVE_TYPES.__contains__(line.split()[0])]

def get_arguments(line):
    """Get list of arguments from a list of strings representing a function declaration line 
    
    Args:
        line ([String]): list of strings representing a function in the format: return_type name arg1 arg2 arg3

    Returns:
        ([String]): list containing all argument types e.g ['int', 'float', 'double'] etc..
    """

    return [arg for arg in line.split()[2:] if Constants.CPP_PRIMITIVE_TYPES.__contains__(arg)]

def clean_function_line(line):
    return Utilities.correct_input(line.replace(";", "").replace("(", " ").replace(")", "").replace("{", ""))

def clean_source(source):
    return Utilities.correct_input(source).splitlines()

def verify_compilation(path, compile_output_dir, compile_output_path, language, individual_assignment):
    """Checks whether a source code for an assignment compiles
    
    Args:
        path (String): path of the source code
        compile_output_dir (String): Output directory of the compilation result
        compile_output_path (String): Output path of the compilation result file
        language (String): Programming language to be compiled

    Returns:
        (boolean, String): Tuple with a flag indicating compilation result and any error messages
    
    """

    Utilities.compile_source(path, compile_output_dir, compile_output_path, language, individual_assignment.get_compile_output_dir() + "main" + Utilities.get_os_file_extension())
    compile_results = Utilities.read_file(compile_output_path)
    Utilities.delete_file(compile_output_path)

    if len(compile_results) < 1:
        return True, None
    return False, compile_results
