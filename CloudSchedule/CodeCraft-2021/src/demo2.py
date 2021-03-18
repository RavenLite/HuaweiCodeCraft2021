import read_file


def divide_type(val, num=0.1):
    if val > 1 + num:
        return 0
    elif val < 1 - num:
        return 1
    else:
        return 2


class Algorithm(object):
    def __init__(self):
        training_data = read_file.get_training_data()
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()

        self.type_num = 3
        self.server_list = [[] for _ in range(self.type_num)]  # 将 server_type_list 划分为三种类型存储
        self.server_save_list = [[] for _ in range(self.type_num)]  # 将已购买的 server_type_list 划分为三种类型存储
        self.server_request_list = []

        self.server_dict = {}
        self.vm_dict = {}

        self.add_queue = []
        self.delete_queue = []

        self.daily_id = 0
        self.server_id = 0
        self.request_id = 0
        self.day = 0

        self.del_request = []

        self.decision = []
        self.vm_id_to_server_id = {}

        self.start_process(self.daily_num, self.daily_queue_list)

    def start_process(self, daily_num, daily_queue_list):
        self.set_server_type()
        for server_list in self.server_list:
            server_list.sort(key = lambda x : x.server_hardware_cost)
        self.get_dict()
        for day in range(daily_num):
            self.daily_id = -1
            self.decision = []
            daily_queue = daily_queue_list[day]
            self.process_daily_queue(daily_queue)

    def process_daily_queue(self, daily_queue):  # 正在写
        for request in daily_queue:
            request.request_id = self.request_id
            request.server_id = -1
            self.request_id += 1
            if request.request_item_action == "add":
                self.process_add_request(request)
            else:
                self.process_delete_request(request)

        self.process_add_queue()
        self.process_delete_queue()
        self.arrange_server_id()
        self.day += 1

    def arrange_server_id(self):
        self.server_request_list.sort(key=lambda x: x.server_name)
        for server in self.server_request_list:
            server.server_id = self.server_id
            self.server_dict[server.server_id] = server
            self.server_id += 1
            for vm in server.vm_include:
                vm.vm_to_server_id = server.server_id

    def process_add_request(self, request):
        vm = self.vm_dict[request.request_item_vm_type]
        request.request_type = vm.vm_type
        request.request_cpu = vm.vm_cpu_num
        request.request_memory = vm.vm_memory_size
        self.add_queue.append(request)

    def process_delete_request(self, request):
        self.delete_queue.append(request)

    def get_dict(self):
        for vm in self.vm_type_list:
            vm.vm_type = divide_type(vm.vm_cpu_num / vm.vm_memory_size)
            self.vm_dict[vm.vm_name] = vm

    def set_server_type(self):
        for server in self.server_type_list:
            flag = divide_type(server.server_cpu_num / server.server_memory_size)
            self.server_list[flag].append(server)

    def process_add_queue(self):
        for request in self.add_queue:
            flag = request.request_type
            vm = self.vm_dict[request.request_item_vm_type]
            vm.type = flag
            vm_append_to_server = read_file.VirtualMachine(
                vm.vm_name, vm.vm_cpu_num, vm.vm_memory_size, vm.vm_memory_size, vm.vm_deployment_way,
                vm.vm_type, vm_to_daily_id=self.daily_id)
            for server in self.server_save_list[flag]:
                if vm.vm_deployment_way == 0:
                    if request.request_cpu <= server.A_rest_cpu_num \
                            and request.request_memory <= server.A_rest_memory_size:
                        server.A_rest_cpu_num -= request.request_cpu
                        server.A_rest_memory_size -= request.request_memory
                        server.vm_include.append(vm_append_to_server)
                        request.server_id = server.server_daily_id
                        decision_append_to_server = read_file.Decision(request.request_id, request.server_id, "A")
                        server.decision = (decision_append_to_server)
                        self.decision.append(decision_append_to_server)
                        break
                    elif request.request_cpu <= server.B_rest_cpu_num \
                            and request.request_memory <= server.B_rest_memory_size:
                        server.B_rest_cpu_num -= request.request_cpu
                        server.B_rest_memory_size -= request.request_memory
                        server.vm_include.append(vm_append_to_server)
                        request.server_id = server.server_daily_id
                        decision_append_to_server = read_file.Decision(request.request_id, request.server_id, "B")
                        server.decision = decision_append_to_server
                        self.decision.append(decision_append_to_server)
                        break
                    else:
                        for purchase_server in self.server_list[flag]:
                            if request.request_cpu <= purchase_server.server_cpu_num / 2 and request.request_memory <= purchase_server.server_memory_size / 2:
                                self.daily_id += 1
                                purchase_server.server_daily_id = self.daily_id
                                purchase_server.day = self.day
                                purchase_server.already_cost = purchase_server.server_hardware_cost
                                self.server_save_list[flag].append(purchase_server)
                                vm_append_to_server.vm_to_daily_id = purchase_server.server_daily_id
                                purchase_server.vm_include.append(vm_append_to_server)
                                purchase_server.A_rest_cpu_num -= request.request_cpu
                                purchase_server.A_rest_memory_size -= request.request_memory
                                request.server_id = purchase_server.server_daily_id
                                decision_append_to_server = read_file.Decision(
                                    request.request_id, request.server_id, "A")
                                purchase_server.decision = decision_append_to_server
                                self.decision.append(decision_append_to_server)
                                self.server_request_list.append(purchase_server)
                                break
                        break
                else:
                    if request.request_cpu / 2 <= server.A_rest_cpu_num and request.request_memory / 2 <= server.A_rest_memory_size:
                        server.A_rest_cpu_num -= request.request_cpu / 2
                        server.A_rest_memory_size -= request.request_memory / 2
                        server.B_rest_cpu_num -= request.request_cpu / 2
                        server.B_rest_memory_size -= request.request_memory / 2
                        server.vm_include.append(vm_append_to_server)
                        request.server_id = server.server_daily_id
                        decision_append_to_server = read_file.Decision(request.request_id, request.server_id, "AB")
                        server.decision = decision_append_to_server
                        self.decision.append(decision_append_to_server)
                        break
                    else:
                        for purchase_server in self.server_list[flag]:
                            if request.request_cpu <= purchase_server.server_cpu_num and request.request_memory <= purchase_server.server_memory_size:
                                self.daily_id += 1
                                request.server_id = purchase_server.server_daily_id
                                purchase_server.day = self.day
                                purchase_server.already_cost = purchase_server.server_hardware_cost
                                self.server_save_list[flag].append(purchase_server)
                                vm_append_to_server.vm_to_daily_id = purchase_server.server_daily_id
                                purchase_server.vm_include.append(vm_append_to_server)
                                purchase_server.A_rest_cpu_num -= request.request_cpu / 2
                                purchase_server.A_rest_memory_size -= request.request_memory / 2
                                purchase_server.B_rest_cpu_num -= request.request_cpu / 2
                                purchase_server.B_rest_memory_size -= request.request_memory / 2
                                request.server_id = purchase_server.server_daily_id
                                decision_append_to_server = read_file.Decision(
                                    request.request_id, request.server_id, "AB")
                                purchase_server.decision = decision_append_to_server
                                self.decision.append(decision_append_to_server)
                                self.server_request_list.append(purchase_server)
                                break
                        break

    def process_delete_queue(self):  # 待修改
        for request in self.delete_queue:
            # flag = request.request_type
            vm = self.vm_dict[request.request_item_vm_type]
            server = self.server_dict[vm.vm_to_server_id]


