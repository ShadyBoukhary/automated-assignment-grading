import os
import sys
import json
from utils.constants import Constants
import errno
import shutil

DEBUG = os.environ['DEBUG']
DEBUG = True if DEBUG == 'True' else False
DEV = os.environ['DEV']
DEV = True if DEV == 'True' else False
SHARED = os.environ['SHARED']


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
    def write_file(filename, str, mode="a"):
        try:
            f = open(filename, mode)
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
    def obj_dict(obj):
        return obj.__dict__

    @staticmethod
    def get_shared_dir():
        return SHARED

    @staticmethod
    def json_serialize(filename, obj):
        try:
            f = open(filename, "w", encoding="utf-8")
            json.dump([ob.to_dict() for ob in obj], f)
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
    def compile_with_cmake(build_dir, build_log_path):
        os.system("cmake -B" + build_dir + " -H" + build_dir + " >temp")
        os.system("make -C " + build_dir + " >temp 2>" + build_log_path)
        Utilities.delete_file("temp")

    @staticmethod
    def create_file_dir_if_not_exists(filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

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
        return Utilities.get_resources_dir() + "assignment_list.json"

    @staticmethod
    def get_resources_dir():
        # if DEV:
        #     return Utilities.get_full_dir_path() + "/../../shared/"
        # else:
        #     from os.path import expanduser
        #     return expanduser("~") + "/resources/"
        return Utilities.get_shared_dir()

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
        # Utilities.append_file(Utilities.get_log_path(), str)
        Utilities.flush()

    @staticmethod
    def Debug(str):
        if DEBUG:
            print(str)

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

    @staticmethod
    def construct_repo_path(current_student):
        return current_student.repo

    @staticmethod
    def get_cmake_template_path():
        return Utilities.get_resources_dir() + "CMakeLists.txt"

    @staticmethod
    def delete_dir_recur(direc):
        if Utilities.path_exists(direc):
            shutil.rmtree(direc)
