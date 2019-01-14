import os
import sys
import json
from utils.constants import Constants

class Utilities:
    """Static class containing utility methods"""

    @staticmethod
    def correct_input(file_contents):
        """Corrects input by removing leading and trailing whitspaces - as well as empty lines"""

        return os.linesep.join([s.strip() for s in file_contents.splitlines() if s]).strip()

    @staticmethod
    def read_file(filename):
        try:
            f = open(filename, "r")
            contents = f.read()
            f.close()
            return Utilities.correct_input(contents)
        except IOError as e:
            print("ERROR: " + e.strerror)
            raise e

    @staticmethod
    def append_file(filename, str):
        try:
            f = open(filename, "a")
            f.write(str + "\n")
        except IOError as e:
            print("ERROR: " + e.strerror)
            raise e

    @staticmethod
    def json_deserialize(filename):
        try:
            f = open(filename, "r")
            contents = json.load(f)
            f.close()
            return contents
        except IOError as e:
            print("FILE ERROR: " + e.strerror + ". FILE: " + filename)
            raise e
        except json.JSONDecodeError as e:
            raise e

    @staticmethod
    def json_serialize(filename, obj):
        try:
            f = open(filename, "w", encoding="utf-8")
            json.dump(obj, f)
            f.close()
        except IOError as e:
            print("FILE ERROR: " + e.strerror)
            raise e
        except json.JSONDecodeError as e:
            print("JSON ERROR: " + str(e))

    @staticmethod
    def run_program(path):            
        os.system(path)

    @staticmethod
    def compile_source(path, output_dir, output_path, language, executable_path):
        if not Utilities.path_exists(output_dir):
            Utilities.create_dir(output_dir)
        if language == "cpp":
            os.system("g++ -o " + executable_path + " " + path + " 2>" + output_path)

    @staticmethod
    def get_os_file_extension():
        """Gets the executable extension according to the OS """

        if sys.platform == Constants.WINDOWS_SYSTEM:
            return ".exe"
        else:
            return ""

    @staticmethod
    def get_home_directory():
        return os.path.expanduser("~")

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)

    @staticmethod
    def get_full_dir_path():
        full_executable_path = os.path.realpath(__file__)
        return os.path.dirname(full_executable_path)

    @staticmethod
    def create_dir(path):
        os.makedirs(path)

    @staticmethod
    def get_assignment_data_file_path():
        return Utilities.get_full_dir_path() + "/../../resources/assignment_list.dat"

    @staticmethod
    def get_log_path():
        path = Utilities.get_full_dir_path() + "/../../logs/log.txt"
        if not Utilities.path_exists(path):
            Utilities.create_dir(Utilities.get_full_dir_path() + "/../../logs/")
        return Utilities.get_full_dir_path() + "/../../logs/log.txt"

    @staticmethod
    def delete_file(path):
        os.remove(path)

    @staticmethod
    def flush():
        sys.stdout.flush()

    @staticmethod
    def log(str, end=False):
        print(str, end="") if end else print(str)
        #Utilities.append_file(Utilities.get_log_path(), str)
        Utilities.flush()

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    @staticmethod
    def simple_string_hash(word):
        return sum(bytearray(word, "utf-8"))