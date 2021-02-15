import os
import platform


def make_directory(directory):
    if not os.path.isfile(directory):
        if not os.path.exists(os.path.dirname(directory)):
            # Create the path to the model if it does not exist
            os.makedirs(os.path.dirname(directory))

        return True

    return False


def make_full_directory(directory):
    if not os.path.isfile(directory):
        if not os.path.exists(directory):
            # Create the path to the model if it does not exist
            os.makedirs(directory)

        return True

    return False


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
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
