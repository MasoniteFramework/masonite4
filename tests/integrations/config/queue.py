DRIVERS = {
    "default": "async",
    "database": {
        "connection": "sqlite",
        "table": "jobs",
        "failed_table": "failed_jobs",
    },
    "redis": {
        #
    },
    "amqp": {
        #
    },
    "async": {"blocking": True},
}
