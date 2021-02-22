"""Helpers to resolve absolute paths to the different app resources using a configured
location."""
from os.path import join, abspath


def _normalize_path(path):
    """Transform dotted path to normal file path."""
    return path.replace(".", "/")


def _build_path(location_key, relative_path, absolute):
    from wsgi import application

    relative_dir = join(_normalize_path(application.make(location_key)), relative_path)
    return abspath(relative_dir) if absolute else relative_dir


def view_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    views location. The relative path can be returned instead by setting absolute=False."""
    return _build_path("views.location", relative_path, absolute)


def controller_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    controllers location. The relative path can be returned instead by setting absolute=False."""
    return _build_path("controller.location", relative_path, absolute)


def config_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    config location. The relative path can be returned instead by setting absolute=False."""
    return _build_path("config.location", relative_path, absolute)


def migrations_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    migrations location. The relative path can be returned instead by setting absolute=False."""
    return _build_path("migrations.location", relative_path, absolute)


def seeds_path(relative_path, absolute=True):
    """Build the absolute path to the given relative_path assuming it exists in the configured
    seeds location. The relative path can be returned instead by setting absolute=False."""
    return _build_path("seeds.location", relative_path, absolute)
