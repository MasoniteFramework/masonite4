def flatten_routes(routes):
    """Flatten the grouped routes into a single list of routes.

    Arguments:
        routes {list} -- This can be a multi dementional list which can flatten all lists into a single list.

    Returns:
        list -- Returns the flatten list.
    """
    route_collection = []
    for route in routes:
        if isinstance(route, list):
            for r in flatten_routes(route):
                route_collection.append(r)
        else:
            route_collection.append(route)

    return route_collection
