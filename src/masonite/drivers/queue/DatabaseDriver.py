import pickle
import pendulum
import inspect
from ...utils.helpers import HasColoredCommands
import time


class DatabaseDriver(HasColoredCommands):
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        return self

    def push(self, *jobs, args=(), **kwargs):
        builder = self.get_builder()

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
                    "available_at": pendulum.now().to_datetime_string(),
                    "attempts": 0,
                    "queue": self.options.get("queue", "default"),
                }
            )

    def consume(self):
        builder = self.get_builder()

        print(self.options.get("attempts"))

        while True:
            time.sleep(int(self.options.get("poll", 1)))
            builder = builder.new().table(self.options.get("table"))
            jobs = (
                builder.where("queue", self.options.get("queue", "default"))
                .where("available_at", "<=", pendulum.now().to_datetime_string())
                .limit(10)
                .order_by("id")
                .get()
            )

            builder.where_in("id", [x["id"] for x in jobs]).update(
                {"reserved_at": pendulum.now().to_datetime_string()}
            )

            for job in jobs:
                builder.where("id", job["id"]).table(self.options.get("table")).update(
                    {
                        "ran_at": pendulum.now().to_datetime_string(),
                    }
                )
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

                    builder.where("id", job["id"]).delete()
                except Exception as e:  # skipcq
                    self.danger(
                        f"[{job['id']}][{pendulum.now().to_datetime_string()}] Job Failed"
                    )

                    if job["attempts"] >= self.options.get("attempts", 1):
                        builder.where("id", job["id"]).delete()
                        if hasattr(obj, "failed"):
                            getattr(obj, "failed")(unserialized, str(e))

                        self.add_to_failed_queue_table(
                            builder, job["name"], payload, str(e)
                        )
                    else:
                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).update(
                            {
                                "attempts": job["attempts"] + 1,
                            }
                        )

    def retry(self):
        builder = self.get_builder()

        jobs = builder.get()

        if len(jobs) == 0:
            self.success("No failed jobs found.")
            return

        for job in jobs:
            builder.table("jobs").create(
                {
                    "name": str(job["name"]),
                    "payload": job["payload"],
                    "attempts": 0,
                    "available_at": pendulum.now().to_datetime_string(),
                    "queue": job["queue"],
                }
            )
        self.success(f"Added {len(jobs)} failed jobs back to the queue")
        builder.table(self.options.get("failed_table", "failed_jobs")).where_in(
            "id", [x["id"] for x in jobs]
        ).delete()

    def get_builder(self):
        return (
            self.application.make("builder")
            .on(self.options.get("connection"))
            .table(self.options.get("table"))
        )

    def add_to_failed_queue_table(self, builder, name, payload, exception):
        builder.table(self.options.get("failed_table", "failed_jobs")).create(
            {
                "driver": "database",
                "queue": self.options.get("queue", "default"),
                "name": name,
                "connection": self.options.get("connection"),
                "created_at": pendulum.now().to_datetime_string(),
                "exception": exception,
                "payload": payload,
                "failed_at": pendulum.now().to_datetime_string(),
            }
        )
