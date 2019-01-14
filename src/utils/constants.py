class Constants:
    """Contains application-wide constants"""

    OUT_TO_FILE = " -a >"
    WINDOWS_SYSTEM = "win32"
    MAC_SYSTEM = "darwin"
    LINUX_SYSTEM = "linux"
    BASE_URL="https://github.com/"
    USERS_URL = "/users"
    REPOS_URL = "/repos"

    USERS_USERNAMES_MAP = {"Shady Boukhary": "shadyboukhary"}
    CLONE_DIRECTORY = "/automated_grading_repos"
    CROSS_MARK = "\u274c"
    CHECK_MARK = "\u2713"
    CPP_PRIMITIVE_TYPES = [
        "short int", "unsigned short int", "unsigned int", "int",
        "long int", "unsigned long int", "long long int", "unsigned long long int",
        "signed char", "char", "unsigned char", "float", "double", "long double", "wchar_t,", "void",
        "string", "std::string"
    ]