
# TrainingData Class, structures each training data
class TrainingData(object):

    def __init__(self, server_type_num, server_type_list, vm_type_num, vm_type_list, daily_num, daily_queue_list):
        # number
        self.server_type_num = server_type_num
        # list of dict
        self.server_type_list = server_type_list
        # number
        self.vm_type_num = vm_type_num
        # list of dict
        self.vm_type_list = vm_type_list
        # number
        self.daily_num = daily_num
        # list of DailyQueue
        self.daily_queue_list = daily_queue_list

    def get_server_type_num(self):
        return self.server_type_num

    def get_server_type_list(self):
        return self.server_type_list

    def get_vm_type_num(self):
        return self.vm_type_num

    def get_vm_type_list(self):
        return self.vm_type_list

    def get_daily_num(self):
        return self.daily_num

    def get_daily_queue_list(self):
        return self.daily_queue_list

    def __str__(self):
        return "server_type_num: {}\nvm_type_num: {}\ndaily_num: {}"\
            .format(self.server_type_num, self.vm_type_num, self.daily_num)

    def check(self):
        return "correctness: " + str(self.server_type_num == len(self.server_type_list)
                                     and self.vm_type_num == len(self.vm_type_list)
                                     and self.daily_num == len(self.daily_queue_list))


class DailyQueue(object):

    def __init__(self, queue_length, queue_info):
        self.daily_queue_length = queue_length
        self.daily_queue_info = queue_info

    def get_daily_queue_length(self):
        return self.daily_queue_length

    def get_daily_queue_info(self):
        return self.daily_queue_info


class QueueItemInfo(object):

    def __init__(self, request_item_action, request_item_vm_type, request_item_vm_id):
        self.request_item_action = request_item_action
        self.request_item_vm_type = request_item_vm_type
        self.request_item_vm_id = request_item_vm_id
        # self.server_id = -1
        # self.request_vm_id = -1
        # self.request_server_id = -1
        self.request_type = -1  # 这个是 cpu memory equal 的分类
        self.request_cpu = -1
        self.request_memory = -1


# class ServerInclude(object):
#
#     def __init__(self, request_item_vm_id, cpu_num, memory_size, department):
#         self.request_item_vm_id = request_item_vm_id
#         self.cpu_num = cpu_num
#         self.memory_size = memory_size
#         self.department = department
#
#
# class PurchaseServer(object):
#
#     def __init__(self, server_id, server_name):
#         self.server_id = server_id
#         self.server_name = server_name


class Decision(object):

    def __init__(self, request_id, server_id, department, request_type="add"):
        self.request_id = request_id
        self.server_id = server_id
        self.department = department
        self.request_type = request_type


class Server(object):

    def __init__(self, server_name, server_cpu_num, server_memory_size, server_hardware_cost, server_energy_cost,
                 server_id=-1, server_daily_id=-1, day=-1, already_cost=0, decision=None):
        self.server_name = server_name
        self.server_cpu_num = server_cpu_num
        self.server_memory_size = server_memory_size
        self.server_hardware_cost = server_hardware_cost
        self.server_energy_cost = server_energy_cost
        self.server_id = server_id
        self.server_daily_id = server_daily_id
        self.A_rest_cpu_num = server_cpu_num / 2
        self.A_rest_memory_size = server_memory_size / 2
        self.B_rest_cpu_num = server_cpu_num / 2
        self.B_rest_memory_size = server_memory_size / 2
        self.vm_include = []
        self.day = day
        self.already_cost = already_cost
        self.decision = decision



class VirtualMachine(object):

    def __init__(self, vm_name, vm_cpu_num, vm_memory_size, vm_deployment_way, vm_type=-1,
                 vm_to_server_id=-1, vm_to_daily_id=-1):
        self.vm_name = vm_name
        self.vm_cpu_num = vm_cpu_num
        self.vm_memory_size = vm_memory_size
        self.vm_deployment_way = vm_deployment_way
        self.vm_type = vm_type
        self.vm_to_server_id = vm_to_server_id
        self.vm_to_daily_id = vm_to_daily_id


def read_file():
    with open('../../training_data/training-1.txt') as f:

        # read server type num
        server_type_num = int(f.readline().strip())

        # read server type list
        server_type_list = []
        for i in range(server_type_num):
            server_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            server_type_list.append(Server(server_type_arr[0], int(server_type_arr[1]), int(server_type_arr[2]),
                                           int(server_type_arr[3]), int(server_type_arr[4])))

        # read vm type num
        vm_type_num = int(f.readline().strip())

        # read server type list
        vm_type_list = []
        for i in range(vm_type_num):
            vm_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            vm_type_list.append(VirtualMachine(vm_type_arr[0], int(vm_type_arr[1]),
                                               int(vm_type_arr[2]), int(vm_type_arr[3])))

        # read day num
        daily_num = int(f.readline().strip())

        # read daily request queue
        request_list = []
        for i in range(daily_num):
            request_queue_length = int(f.readline().strip())
            request_queue_list = []
            for j in range(request_queue_length):
                request_item_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
                request_queue_list.append(QueueItemInfo(
                    request_item_arr[0],
                    request_item_arr[1] if request_item_arr[0] == "add" else "",
                    int(request_item_arr[2] if request_item_arr[0] == "add" else request_item_arr[1]))
                )

            daily_queue = DailyQueue(request_queue_length, request_queue_list)
            request_list.append(daily_queue)

    return TrainingData(server_type_num, server_type_list, vm_type_num, vm_type_list, daily_num, request_list)


def get_training_data():
    training_data = read_file()
    print(training_data)
    print(training_data.check())
    return training_data


if __name__ == "__main__":
    get_training_data()
