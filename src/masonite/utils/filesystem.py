import os
import platform
import shutil


def make_directory(directory):
    """Create a directory at the given path for a file if it does not exist"""
    if not os.path.isfile(directory):
        if not os.path.exists(os.path.dirname(directory)):
            # Create the path to the model if it does not exist
            os.makedirs(os.path.dirname(directory))

        return True

    return False


def file_exists(directory):
    """Create a directory at the given path for a file if it does not exist"""
    return os.path.exists(os.path.dirname(directory))


def make_full_directory(directory):
    """Create all directories to the given path if they do not exist"""
    if not os.path.isfile(directory):
        if not os.path.exists(directory):
            # Create the path to the model if it does not exist
            os.makedirs(directory)

        return True

    return False


def creation_date(path_to_file):
    """Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    """
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def modified_date(path_to_file):
    if platform.system() == "Windows":
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_mtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return 0


def copy_file_or_append(from_location, to_location):
    if not os.path.isfile(to_location):
        shutil.copyfile(from_location, to_location)
    else:
        with open(from_location, "r") as from_file_pointer, open(
            os.path.join(os.getcwd(), to_location), "a"
        ) as to_file_pointer:
            to_file_pointer.write(from_file_pointer.read())
