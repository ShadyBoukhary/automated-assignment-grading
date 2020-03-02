from colorama import Fore


class Constants:
    """Contains application-wide constants"""

    OUT_TO_FILE = " -a >"
    WINDOWS_SYSTEM = "win32"
    MAC_SYSTEM = "darwin"
    LINUX_SYSTEM = "linux"
    BASE_URL = "https://github.com/"

    CLONE_DIRECTORY = "/automated_grading_repos"
    CROSS_MARK = "\u274c"
    CHECK_MARK = Fore.GREEN + "\u2713"
    LEVENSHTEIN_DISTANCE = 3
    CPP_PRIMITIVE_TYPES = [
        "short int", "unsigned short int", "unsigned int", "int",
        "long int", "unsigned long int", "long long int", "unsigned long long int",
        "signed char", "char", "unsigned char", "float", "double", "long double", "wchar_t,", "void",
        "string", "std::string"
    ]

    # CMAKE
    CMAKE_PROJECT_NAME = "REPLACE_PROJECT_NAME"
    CMAKE_EXECUTABLE_NAME = "REPLACE_EXECUTABLE_NAME"
    CMAKE_INCLUDE_DIRS = "REPLACE_INCLUDE_DIRS"
    CMAKE_SOURCE_GLOB = "REPLACE_SOURCE_GLOB"
    CMAKE_OUTPUT_DIR = "REPLACE_OUTPUT_DIRECTORY"

    # RegEx
    RUBRIC_REGEX = r"(?i)(\bREPLACE\b)\s*[=:][\s&$%#]*(\d+[.]?\d*|[\w\s][^\n]+)"
