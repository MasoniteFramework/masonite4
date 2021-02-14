"""Helpers to resolve absolute paths to the different app resources using a configured
location."""
from os.path import join, abspath


def view_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    views location. The relative path can be returned instead by setting absolute=False."""
    from wsgi import application
    relative_dir = join(application.make("views.location"), relative_path)
    return abspath(relative_dir) if absolute else relative_dir


def controller_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    controllers location. The relative path can be returned instead by setting absolute=False."""
    from wsgi import application
    relative_dir = join(application.make("controller.location"), relative_path)
    return abspath(relative_dir) if absolute else relative_dir
