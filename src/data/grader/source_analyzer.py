from core.assignment import Assignment
from core.function import Function
from core.individual_assignment import IndividualAssignment
from core.source_report import SourceReport
from custom.compilation_exception import CompilationException
from utils.constants import Constants
from utils.utilities import Utilities
import glob



def analyze_source(sources_path, assignment, individual_assignment):
    """
    Analyzes a source file. Checks if the source file compiles, compiles it, 
    finds all functions present in the source file and gathers their signiture.
    If the file does not compile, a CompilationException is raised.

    Args:
        sources_path (String)                           : The directory of the source files
        assignment (Assignment)                         : The course assignment being graded.
        individual_assignment (IndividualAssignment)    : The student assignment being evaluated and analyzed

    Returns: 
        (SourceReport)                                  : The report about the source containing function information

    Raises:
        (CompilationException)                          : If the source file does not compile
    
    """

    Utilities.log("Compiling... ", True)
    Utilities.flush()
    try:
        result, error = verify_compilation(sources_path, individual_assignment.get_compile_output_dir(), individual_assignment.get_compile_output_path(), "cpp", individual_assignment)
        if result:
            sources = read_sources_and_headers(sources_path)
            # TODO: Keep track of functions in source, maybe loops too?
            source_report = analyze(sources, "cpp")
            Utilities.log(Constants.CHECK_MARK)
            return source_report
        else:
            raise CompilationException(Constants.CROSS_MARK, error)
    except IOError as e:
        Utilities.log(e)


def analyze(sources, language):
    sources = clean_sources(sources)

    if language == "cpp":
        return analyze_cpp(sources)


def analyze_cpp(sources):
    """
    Analyzes C++ source files. Finds all function declaration and generates a 
    report based on the functions found.
    
    Args:
        sources ([String])  : a list of contents of each source file

    Returns:
        SourceReport        : the report generated using the given source files' contents
    
     """
    source_report = SourceReport(Constants.CPP_PRIMITIVE_TYPES)

    # for every source/header file contents
    for source in sources:
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
    """
    Get list of arguments from a list of strings representing a function declaration line 
    
    Args:
        line ([String]) : List of strings representing a function in the format: return_type name arg1 arg2 arg3

    Returns:
        ([String])      : List containing all argument types e.g ['int', 'float', 'double'] etc..
    """

    return [arg for arg in line.split()[2:] if Constants.CPP_PRIMITIVE_TYPES.__contains__(arg)]

def clean_function_line(line):
    return Utilities.correct_input(line.replace(";", "").replace("(", " ").replace(")", "").replace("{", ""))

def clean_source(source):
    return Utilities.correct_input(source).splitlines()

def clean_sources(sources):
    """
    Cleans a list of sources from extra empty lines 
    
    Args:
        sources ([String])  : The list of source file contents

    Returns:
        ([String])          : The clean list of source file contents
    
    """
    return [clean_source(source) for source in sources]

def verify_compilation(path, compile_output_dir, compile_output_path, language, individual_assignment):
    """
    Checks whether a source code for an assignment compiles
    
    Args:
        path (String)                   : path of the source code
        compile_output_dir (String)     : Output directory of the compilation result
        compile_output_path (String)    : Output path of the compilation result file
        language (String)               : Programming language to be compiled

    Returns:
        (boolean, String)               : Tuple with a flag indicating compilation result and any error messages
    
    """

    executable_name = "main" + Utilities.get_os_file_extension()
    
    init_cmake(path, path, individual_assignment.name, executable_name, compile_output_dir)

    Utilities.compile_with_cmake(compile_output_dir, compile_output_path)
    compile_results = Utilities.read_file(compile_output_path)

    #Utilities.delete_file(compile_output_path)

    if len(compile_results) < 1:
        return True, None
    return False, compile_results

def init_cmake(source_dir, include_dir, assignment_name, executable_name, output_dir):
    """
    Prepares the CMAKE build sytem for the assignment. Copies the template CMAKE file from resources 
    to the compile-temp/ directory for the assignment. Then, it replaces the placeholders with the
    required information for CMAKE, including the source globs, include directories, project name,
    executable name, and output directory.

    Args:
        source_dir (String)         : The directory in which the source files are located
        include_dir (String)        : The directory in which the header files are located
        assignment_name (String)    : The name of the assignment being evaluated
        executable_name (String)    : The name of the executable file to be generated
        output_dir (String)         : The output directory where the executable is generated


    """
    cmake_contents = Utilities.read_file(Utilities.get_cmake_template_path())

    # replace placeholder cmake variables and directories
    cmake_contents = cmake_contents.replace(Constants.CMAKE_SOURCE_GLOB, "\"" + source_dir + "*.cpp\"")
    cmake_contents = cmake_contents.replace(Constants.CMAKE_INCLUDE_DIRS, include_dir)
    cmake_contents = cmake_contents.replace(Constants.CMAKE_PROJECT_NAME, assignment_name)
    cmake_contents = cmake_contents.replace(Constants.CMAKE_EXECUTABLE_NAME, executable_name)
    cmake_contents = cmake_contents.replace(Constants.CMAKE_OUTPUT_DIR, "\"" + output_dir + "\"")

    new_cmake_path = output_dir + "CMakeLists.txt"

    if not Utilities.path_exists(output_dir):
        Utilities.create_dir(output_dir)
    Utilities.write_file(new_cmake_path, cmake_contents, "w")

        
def read_sources_and_headers(directory, language="cpp"):
    if language == "cpp":
        sources = glob.glob(directory + "*.cpp")
        headers = glob.glob(directory + "*.h")
        
        contents = [Utilities.read_file(source) for source in sources] + [Utilities.read_file(header) for header in headers]
        return contents