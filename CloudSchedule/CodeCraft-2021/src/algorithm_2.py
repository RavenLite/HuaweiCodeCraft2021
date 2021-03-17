import read_file


class Algorithm:
    def __init__(self):
        training_data = read_file.get_training_data()

        # 原始数据
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()

    def start_process(self):
        pass

    def set_server_attribute(self):
        for i in range(self.server_type_num):
            self.server_type_list[i]["ability"] = self.server_type_list[i]


# all time variable
class ResourcePool:

    def __init__(self):
        pass
