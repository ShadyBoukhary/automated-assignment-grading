from colorama import Fore
from PyInquirer import style_from_dict, Token


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

    # Command help
    STUDENT_HELP = '''
The rubric file to be used for the assignment. Must be in json format
Example:
[
{
"firstName":"Paige",
"lastName":"Champaigne",
"username":"paigechampagne"
},
{
"firstName":"Chris",
"lastName":"Something",
"username":"chris473"
},
{
"firstName":"Blake",
"lastName":"Wilson",
"username":"BlakeWilson"
},
{
"firstName":"Shady",
"lastName":"Boukhary",
"username":"shadyboukhary"
}
]
    '''

    RUBRIC_HELP = '''
[
{
"key":"subtotal",
"value":9350.00,
"weight":33.33
},
{
"key":"tax amount",
"value":771.38,
"weight":33.33
}
]
'''

# Styles

    STYLE = style_from_dict({
                Token.Separator: '#cc5454',
                Token.QuestionMark: '#673ab7 bold',
                Token.Selected: '#cc5454',  # default
                Token.Pointer: '#673ab7 bold',
                Token.Instruction: '',  # default
                Token.Answer: '#f44336 bold',
                Token.Question: '',
            })