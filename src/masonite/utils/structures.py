"""Helpers for multiple data structures"""
import pydoc
from dotty_dict import dotty

from .str import modularize


def load(path, object, default=None):
    """Load the given object from a Python module located at path and returns a default
    value if not found.

    Arguments:
        path {str} -- A file path or a dotted path of a Python module
        object {str} -- The object name to load in this module
        default {str} -- The default value to return if object not found in module (None)

    Returns:
        {object} -- The value (or default) read in the module
    """
    # modularize path if needed
    dotted_path = modularize(path)
    module = pydoc.locate(dotted_path)
    return getattr(module, object, default)


def data(dictionary={}):
    """Transform the given dictionary to be read/written with dot notation.

    Arguments:
        dictionary {dict} -- a dictionary structure

    Returns:
        {dict} -- A dot dictionary
    """
    return dotty(dictionary)


def data_get(dictionary, key, default=None):
    """Read dictionary value from key using nested notation.

    Arguments:
        dictionary {dict} -- a dictionary structure
        key {str} -- the dotted (or not) key to look for
        default {object} -- the default value to return if the key does not exist (None)

    Returns:
        value {object}
    """
    # dotty dict uses : instead of * for wildcards
    dotty_key = key.replace("*", ":")
    return data(dictionary).get(dotty_key, default)


def data_set(dictionary, key, value, overwrite=True):
    """Set dictionary value at key using nested notation. Values are overriden by default but
    this behaviour can be changed by passing overwrite=False.
    The dictionary is edited in place but is also returned.

    Arguments:
        dictionary {dict} -- a dictionary structure
        key {str} -- the dotted (or not) key to set
        value {object} -- the value to set at key
        overwrite {bool} -- override the value if key exists in dictionary (True)

    Returns:
        dictionary {dict} -- the edited dictionary
    """
    if "*" in key:
        raise ValueError("You cannot set values with wildcards *")
    if not overwrite and data_get(dictionary, key):
        return
    data(dictionary)[key] = value
    return dictionary
