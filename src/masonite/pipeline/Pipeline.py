class Pipeline:
    def __init__(self, payload):
        self.payload = payload

    def through(self, pipe_list):
        passthrough = self.payload
        for pipe in pipe_list:
            response = pipe().handle(self.payload)
            if response != passthrough:
                break
