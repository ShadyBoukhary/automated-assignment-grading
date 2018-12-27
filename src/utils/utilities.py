import os
import sys
from utils.constants import Constants

class Utilities:
    """Static class containing utility methods"""

    @staticmethod
    def correct_input(file_contents):
        """Corrects input by removing leading and trailing whitspaces - as well as empty lines"""

        return os.linesep.join([s for s in file_contents.splitlines() if s]).strip()

    @staticmethod
    def read_file(filename):
        try:
            f = open(filename, "r")
            contents = f.read()
            f.close()
            return Utilities.correct_input(contents)
        except IOError as e:
            print("ERROR: " + e.strerror)
            sys.exit()

    @staticmethod
    def run_program(path):
        os.system(path)

    @staticmethod
    def get_os_file_extension():
        """Gets the executable extension according to the OS """

        if os.system == Constants.WINDOWS_SYSTEM:
            return ".exe"
        else:
            return ""

    @staticmethod
    def get_home_directory():
        return os.path.expanduser("~")

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)
