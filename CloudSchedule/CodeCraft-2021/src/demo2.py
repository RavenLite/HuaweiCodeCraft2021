import read_file

# server_type = {
#     "server_name": server_type_arr[0],
#     "server_cpu_num": int(server_type_arr[1]),
#     "server_memory_size": int(server_type_arr[2]),
#     "server_hardware_cost": int(server_type_arr[3]),
#     "server_energy_cost": int(server_type_arr[4])
# }

# vm_type = {
#     "vm_name": vm_type_arr[0],
#     "vm_cpu_num": int(vm_type_arr[1]),
#     "vm_memory_size": int(vm_type_arr[2]),
#     "vm_deployment_way": int(vm_type_arr[3]),
# }

# action = {
#     "request_item_action": request_item_arr[0],
#     "request_item_vm_type": request_item_arr[1] if request_item_arr[0] == "add" else "",
#     "request_item_vm_id": int(request_item_arr[2] if request_item_arr[0] == "add" else request_item_arr[1])
# }

class Algorithm(object):
    def __init__(self):
        training_data = read_file.get_training_data()
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()

        self.server_type_more_cpu = []
        self.server_type_more_memory = []
        self.server_type_equal = []

        self.server_save_more_cpu = {}
        self.server_save_more_memory = {}
        self.server_save_equal = {}

        self.daily_id = 0
        self.server_id = 0

        self.add_more_cpu = {}
        self.add_more_memory = {}
        self.add_equal = {}

        self.del_request = []

        self.start_process(self.daily_num, self.daily_queue_list)

    def start_process(self, daily_num, daily_queue_list):
        for day in range(daily_num):
            self.daily_id = 0
            daily_queue = daily_queue_list[day]
            for action in daily_queue:
                self.process_daily_queue(action)

    def process_daily_queue(self, action):
        self.set_server_type()

        while True:
            if action["request_item_action"] == "add":
                self.process_add_request()
            else:
                self.process_delete_request()

        self.arrange_server_id()

    def arrange_server_id(self):
        pass

    def process_add_request(self):



        #TODO
        self.daily_id += 1

    def process_delete_request(self):
        pass

    def set_server_type(self):
        for server in self.server_type_list:
            # num 用于修正分类比值
            val = server["server_cpu_num"] / server["server_memory_size"]
            num = 0
            if val > 1 + num:
                self.server_type_more_cpu.append(server)
            elif val < 1 - num:
                self.server_type_more_memory.append(server)
            else:
                self.server_type_equal.append(server)

class Server(object):
    def __init__(self):
        self.server_name = ""
        self.server_cpu_num = 0
        self.server_memory_size = 0
        self.server_hardware_cost = 0
        self.server_energy_cost = 0

        self.server_id = 0
        self.daily_id = 0

        self.vm_list = {}

    def getNewServer(self, server_type, daily_id):
        self.server_name = server_type["server_name"]
        self.server_cpu_num = server_type["server_cpu_num"]
        self.server_memory_size = server_type["server_memory_size"]
        self.server_hardware_cost = server_type["server_hardware_cost"]
        self.server_energy_cost = server_type["server_energy_cost"]
        self.daily_id = daily_id

    def setVm(self, vm_type, vm_id):




class Vm(object):
    def __init__(self):
        self.vm_name = ""
        self.vm_cpu_num = 0
        self.vm_memory_size = 0
        self.vm_deployment_way = 0
        self.server_deployment = 0
        self.vm_id = 0

    def getNewVm(self):
