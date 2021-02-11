DRIVERS = {
    "default": "async",
    "database": {
        "connection": "sqlite",
        "table": "jobs",
        "failed_table": "failed_jobs",
        "attempts": 3,
        "poll": 5
    },
    "redis": {
        #
    },
    "amqp": {
        #
    },
    "async": {"blocking": True},
}
