DRIVERS = {
    "default": "async",
    "database": {
        "connection": "sqlite",
        "table": "jobs",
        "failed_table": "failed_jobs",
        "attempts": 3,
    },
    "redis": {
        #
    },
    "amqp": {
        #
    },
    "async": {"blocking": True},
}
