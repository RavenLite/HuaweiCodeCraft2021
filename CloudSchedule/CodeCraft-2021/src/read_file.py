import constant


# TrainingData Class, structures each training data of basic input
class TrainingData(object):

    def __init__(self, server_type_num, server_type_list, vm_type_num, vm_type_list, daily_queue_num, daily_queue_list):
        self.server_type_num = server_type_num
        self.server_type_list = server_type_list
        self.vm_type_num = vm_type_num
        self.vm_type_list = vm_type_list
        self.daily_queue_num = daily_queue_num
        self.daily_queue_list = daily_queue_list

    def __str__(self):
        return "server_type_num: {}\nvm_type_num: {}\ndaily_num: {}"\
            .format(self.server_type_num, self.vm_type_num, self.daily_queue_num)

    def check(self):
        return "correctness: " + str(self.server_type_num == len(self.server_type_list)
                                     and self.vm_type_num == len(self.vm_type_list)
                                     and self.daily_queue_num == len(self.daily_queue_list))


class DailyQueue(object):

    def __init__(self, queue_item_num, queue_item_list):
        # basic field | 来自于标准输入的基本属性
        self.queue_item_num = queue_item_num
        self.queue_item_list = queue_item_list


class QueueItem(object):

    def __init__(self, queue_item_action, queue_item_vm_type_name, queue_item_vm_id):
        # basic field | 来自于标准输入的基本属性
        self.queue_item_action = queue_item_action
        self.queue_item_vm_type_name = queue_item_vm_type_name
        self.queue_item_vm_id = queue_item_vm_id

        # 中间变量
        self.server_daily_id = -1
        self.server_node = constant.NULL_STRING


class ServerType(object):

    def __init__(self, server_type_name, server_type_cpu_num, server_type_memory_size,
                 server_type_hardware_cost, server_type_energy_cost):
        # basic field | 来自于标准输入的基本属性
        self.server_type_name = server_type_name
        self.server_type_cpu_num = server_type_cpu_num
        self.server_type_memory_size = server_type_memory_size
        self.server_type_hardware_cost = server_type_hardware_cost
        self.server_type_energy_cost = server_type_energy_cost

        # assisted field | 算法相关的属性
        self.server_type_ratio = round(self.server_type_cpu_num / self.server_type_memory_size, 2)


class VirtualMachineType(object):

    def __init__(self, vm_type_name, vm_type_cpu_num, vm_type_memory_size, vm_type_deployment_way):
        # basic field | 来自于标准输入的基本属性
        self.vm_type_name = vm_type_name
        self.vm_type_cpu_num = vm_type_cpu_num
        self.vm_type_memory_size = vm_type_memory_size
        self.vm_type_deployment_way = vm_type_deployment_way

        # assisted field | 算法相关的属性
        self.vm_type_ratio = round(self.vm_type_cpu_num / self.vm_type_memory_size, 2)


class Server(object):

    def __init__(self, server_type):
        self.server_type = server_type
        self.server_id = constant.VIRTUAL_SERVER_ID
        self.server_cpu_num_left_a = server_type.server_type_cpu_num / 2
        self.server_memory_size_left_a = server_type.server_type_memory_size / 2
        self.server_cpu_num_left_b = server_type.server_type_cpu_num / 2
        self.server_memory_size_left_b = server_type.server_type_memory_size / 2


class VirtualMachine(object):

    def __init__(self, vm_type):
        self.vm_type = vm_type
        self.vm_id = -1


def read_file():
    with open('../../training_data/training-2.txt') as f:

        # read server type num
        server_type_num = int(f.readline().strip())

        # read server type list
        server_type_list = []
        for i in range(server_type_num):
            server_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            server_type_list.append(ServerType(server_type_arr[0], int(server_type_arr[1]), int(server_type_arr[2]),
                                               int(server_type_arr[3]), int(server_type_arr[4])))

        # read vm type num
        vm_type_num = int(f.readline().strip())

        # read server type list
        vm_type_list = []
        for i in range(vm_type_num):
            vm_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            vm_type_list.append(VirtualMachineType(vm_type_arr[0], int(vm_type_arr[1]),
                                                   int(vm_type_arr[2]), int(vm_type_arr[3])))

        # read daily queue num
        daily_queue_num = int(f.readline().strip())

        # read daily queue list
        daily_queue_list = []
        for i in range(daily_queue_num):
            queue_item_num = int(f.readline().strip())
            queue_item_list = []
            for j in range(queue_item_num):
                request_item_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
                queue_item_list.append(QueueItem(
                    request_item_arr[0],
                    request_item_arr[1] if request_item_arr[0] == "add" else "",
                    int(request_item_arr[2] if request_item_arr[0] == "add" else request_item_arr[1]))
                )

            daily_queue = DailyQueue(queue_item_num, queue_item_list)
            daily_queue_list.append(daily_queue)

    return TrainingData(server_type_num, server_type_list, vm_type_num, vm_type_list, daily_queue_num, daily_queue_list)


def get_training_data():
    training_data = read_file()
    return training_data


if __name__ == "__main__":
    get_training_data()
