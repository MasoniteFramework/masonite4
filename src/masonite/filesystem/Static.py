"""Static Helper Module."""


def static(alias, file_name):
    """Get the static file location of an asset.

    Arguments:
        alias {string} -- The driver and location to search for. This could be s3.uploads
        file_name {string} -- The filename of the file to return.

    Returns:
        string -- Returns the file location.
    """
    from wsgi import application

    store_config = application.make("storage").store_config
    import pdb

    pdb.set_trace()
    return application.make("storage").disk(alias).get(file_name)
    # import pdb

    # pdb.set_trace()
    # store_config.get("alias").

    # if "." in alias:
    #     alias = alias.split(".")
    #     location = DRIVERS[alias[0]]["location"][alias[1]]
    #     if location.endswith("/"):
    #         location = location[:-1]

    #     return "{}/{}".format(location, file_name)

    # location = DRIVERS[alias]["location"]
    # if isinstance(location, dict):
    #     location = list(location.values())[0]
    #     if location.endswith("/"):
    #         location = location[:-1]

    # return "{}/{}".format(location, file_name)