import read_file


def read():
    server_type_num = int(input())
    server_type_list = []
    for i in range(server_type_num):
        server_type_arr = input().strip().replace("(", "").replace(")", "").split(", ")
        server_type_dict = {
            "server_name": server_type_arr[0],
            "server_cpu_num": int(server_type_arr[1]),
            "server_memory_size": int(server_type_arr[2]),
            "server_hardware_cost": int(server_type_arr[3]),
            "server_energy_cost": int(server_type_arr[4])
        }
        server_type_list.append(server_type_dict)

    # read vm type num
    vm_type_num = int(input().strip())

    # read server type list
    vm_type_list = []
    for i in range(vm_type_num):
        vm_type_arr = input().strip().replace("(", "").replace(")", "").split(", ")
        vm_type_dict = {
            "vm_name": vm_type_arr[0],
            "vm_cpu_num": int(vm_type_arr[1]),
            "vm_memory_size": int(vm_type_arr[2]),
            "vm_deployment_way": int(vm_type_arr[3]),
        }
        vm_type_list.append(vm_type_dict)

    # read day num
    daily_num = int(input().strip())

    # read daily request queue
    request_list = []
    for i in range(daily_num):
        request_queue_length = int(input().strip())
        request_queue_list = []
        for j in range(request_queue_length):
            request_item_arr = input().strip().replace("(", "").replace(")", "").split(", ")
            request_item_info = {
                "request_item_action": request_item_arr[0],
                "request_item_vm_type": request_item_arr[1] if request_item_arr[0] == "add" else "",
                "request_item_vm_id": int(request_item_arr[2] if request_item_arr[0] == "add" else request_item_arr[1])
            }
            request_queue_list.append(request_item_info)

        daily_queue = read_file.DailyQueue(request_queue_length, request_queue_list)
        request_list.append(daily_queue)

    return read_file.TrainingData(server_type_num, server_type_list, vm_type_num, vm_type_list, daily_num, request_list)


def get_training_data():
    training_data = read()
    # print(training_data)
    # print(training_data.check())
    return training_data


if __name__ == "__main__":
    get_training_data()
