import pickle
import pendulum
import inspect
from ...utils.helpers import HasColoredCommands


class DatabaseDriver(HasColoredCommands):
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        return self

    def push(self, *jobs, args=(), **kwargs):
        builder = (
            self.application.make("builder")
            .on(self.options.get("connection"))
            .table(self.options.get("table"))
        )

        for job in jobs:
            payload = pickle.dumps(
                {
                    "obj": job,
                    "args": args,
                    "kwargs": kwargs,
                    "callback": self.options.get("callback", "handle"),
                }
            )

            builder.create(
                {
                    "name": str(job),
                    "payload": payload,
                    "serialized": payload,
                    "attempts": 0,
                    "queue": self.options.get("queue", "default"),
                }
            )

    def consume(self):
        builder = (
            self.application.make("builder")
            .on(self.options.get("connection"))
            .table(self.options.get("table"))
        )

        # print(builder)
        jobs = (
            builder.where_null("ran_at")
            .where_null("reserved_at")
            .where("queue", self.options.get("queue", "default"))
            .where(
                lambda q: q.where_null("available_at").or_where(
                    "available_at", "<=", pendulum.now().to_datetime_string()
                )
            )
            .limit(10)
            .order_by("id")
            .get()
        )

        # builder.where_in("id", [x['id'] for x in jobs]).update(
        #     {"reserved_at": pendulum.now().to_datetime_string()}
        # )

        for job in jobs:
            # builder.where("id", job["id"]).update(
            #     {
            #         "ran_at": pendulum.now().to_datetime_string(),
            #     }
            # )
            payload = job["payload"]
            unserialized = pickle.loads(job["payload"])
            obj = unserialized["obj"]
            args = unserialized["args"]
            callback = unserialized["callback"]

            try:
                try:
                    if inspect.isclass(obj):
                        obj = container.resolve(obj)

                    getattr(obj, callback)(*args)

                except AttributeError:
                    obj(*args)

                self.success(
                    f"[{job['id']}][{pendulum.now().to_datetime_string()}] Job Successfully Processed"
                )
                return 2 / 0
                builder.where("id", job["id"]).delete()
            except Exception as e:  # skipcq
                # raise e
                self.danger(
                    f"[{job['id']}][{pendulum.now().to_datetime_string()}] Job Failed"
                )

                if hasattr(obj, "failed"):
                    getattr(obj, "failed")(unserialized, str(e))

                self.add_to_failed_queue_table(builder, payload, str(e))

    def add_to_failed_queue_table(self, builder, payload, exception):
        builder.table("failed_jobs").create(
            {
                "driver": "database",
                "queue": self.options.get("queue", "default"),
                "connection": self.options.get("connection"),
                "exception": exception,
                "payload": payload,
                "failed_at": pendulum.now().to_datetime_string(),
            }
        )
