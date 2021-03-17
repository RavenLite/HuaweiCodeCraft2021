
class Algorithm(object):
    def __init__(self):
        pass

    def start_process(self):
        self.process_daily_queue()

    def process_daily_queue(self, action):
        self.set_server_type()

        while True:
            if action == "add":
                self.process_add_request()
            else:
                self.process_delete_request()

        self.arrange_server_id()

    def arrange_server_id(self):
        pass

    def process_add_request(self):
        server_daily_id = 0

        #TODO

        return server_daily_id

    def process_delete_request(self):
        pass

    def set_server_type(self):
        pass
