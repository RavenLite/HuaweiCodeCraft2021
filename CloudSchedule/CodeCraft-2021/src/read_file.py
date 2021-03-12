
# TrainingData Class, structures each training data
class TrainingData(object):

    def __init__(self, server_type_num, server_type_list, vm_type_num, vm_type_list, daily_num, daily_queue_list):
        # number
        self.server_type_num = int(server_type_num)
        # list of tuple
        self.server_type_list = server_type_list
        # number
        self.vm_type_num = int(vm_type_num)
        # list of tuple
        self.vm_type_list = vm_type_list
        # number
        self.daily_num = int(daily_num)
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
        # number
        self.daily_queue_length = queue_length
        # list of tuple
        self.daily_queue_info = queue_info

    def get_daily_queue_length(self):
        return self.daily_queue_length

    def get_daily_queue_info(self):
        return self.daily_queue_info


def read_file():
    with open('../../training_data/training-1.txt') as f:

        # read server type num
        server_type_num = f.readline().strip()

        # read server type list
        server_type_list = []
        for i in range(int(server_type_num)):
            server_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            server_type_dict = {
                "server_name": server_type_arr[0],
                "server_cpu_num": int(server_type_arr[1]),
                "server_memory_size": int(server_type_arr[2]),
                "server_hardware_cost": int(server_type_arr[3]),
                "server_energy_cost": int(server_type_arr[4])
            }
            server_type_list.append(server_type_dict)

        # read vm type num
        vm_type_num = f.readline().strip()

        # read server type list
        vm_type_list = []
        for i in range(int(vm_type_num)):
            vm_type_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
            vm_type_dict = {
                "vm_name": vm_type_arr[0],
                "vm_cpu_num": int(vm_type_arr[1]),
                "vm_memory_size": int(vm_type_arr[2]),
                "vm_deployment_way": int(vm_type_arr[3]),
            }
            vm_type_list.append(vm_type_dict)

        # read day num
        daily_num = f.readline().strip()

        # read daily request queue
        request_list = []
        for i in range(int(daily_num)):
            request_queue_length = f.readline().strip()
            request_queue_list = []
            for j in range(int(request_queue_length)):
                request_item_arr = f.readline().strip().replace("(", "").replace(")", "").split(", ")
                request_item_info = {
                    "request_item_action": request_item_arr[0],
                    "request_item_vm_type": request_item_arr[1] if request_item_arr[0] == "add" else "",
                    "request_item_vm_id": request_item_arr[2] if request_item_arr[0] == "add" else request_item_arr[1]
                }
                request_queue_list.append(request_item_info)

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
