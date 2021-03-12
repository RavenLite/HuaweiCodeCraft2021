import read_file


class algorithm(object):

    def __init__(self):
        training_data = read_file.get_training_data()
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()

        # 格式：{server_id : server_type_dict}
        self.server_map = {}
        # 格式：[server_id]
        self.server_list = []
        # 格式：[server_id]
        self.work_server_list = []
        # 格式：[server_id]
        self.idle_server_list = []
        # 总支出
        self.cost = 0
        # 当前 server_id
        self.server_id = 0
        # 格式：{vm_id : server_id}
        self.vm_map = {}
        # 格式：{request_item_vm_type : server_type_dict}
        self.best_server_for_vm = {}
        # 格式：{vm_name : vm_deployment_way}
        self.vm_is_or_not_partition = {}

        self.deal_with_daily_queue()

    def deal_with_daily_queue(self):
        self.get_best_server_for_vm()
        self.get_vm_is_or_not_partition()

        # 构建输出列表
        purchase_list = []
        migration_list = []
        create_list = []
        delete_list = []

        for daily_queue in self.daily_queue_list:
            for request in daily_queue.get_daily_queue_info():

                # 添加虚拟机
                if request["request_item_action"] == "add":
                    flag = False
                    server_id = -1

                    # 首先检查是否存在未使用的最佳服务器
                    for server in self.idle_server_list:
                        if self.server_map[server] == self.best_server_for_vm[request["request_item_vm_type"]]:
                            flag = True
                            server_id = server
                            break

                    # 存在未使用服务器，拿来用
                    if flag:
                        self.idle_server_list.remove(server_id)
                        self.work_server_list.append(server_id)

                    # 不存在，购买新服务器
                    else:
                        best_server = self.best_server_for_vm[request["request_item_vm_type"]]
                        flag = False
                        j = -1
                        for i in purchase_list:
                            if best_server in i:
                                flag = True

                        # 加入购买队列
                        if flag:
                            purchase_list[j][1] += 1
                        else:
                            purchase_list.append((best_server, 1))
                        server_id = self.server_id - 1

                    # 加入添加队列
                    create = [server_id]
                    if self.vm_is_or_not_partition[request["request_item_vm_type"]] == 0:
                        create.append("A")
                    create_list.append(create)


                # 删除虚拟机
                else:
                    del_vm_server_id = self.vm_map.pop(request["request_item_vm_id"])
                    self.work_server_list.remove(del_vm_server_id)
                    self.idle_server_list.append(del_vm_server_id)

        # 执行输出
        self.purchase(purchase_list)
        self.migration(migration_list)
        self.create(create_list)
        self.delete(delete_list)

    def get_vm_is_or_not_partition(self):
        for vm in self.vm_type_list:
            self.vm_is_or_not_partition["{}".format(vm["vm_name"])] = vm["vm_deployment_way"]

    def get_best_server_for_vm(self):
        # 对服务器分别按照 价格， cpu 和 memory 排序
        # server_sort_by_cpu = sorted(self.server_type_list, key=lambda x: x["server_cpu_num"])
        # server_sort_by_memory = sorted(self.server_type_list, key=lambda x: x["server_memory_size"])
        server_sort_by_hardware_cost = sorted(self.server_type_list, key = lambda x : x["server_hardware_cost"], reverse = True)

        for vm in self.vm_type_list:

            # 这里需要根据 vm 是否是双节点做一个判断
            denominator = 1 if vm["vm_deployment_way"] == 1 else 2
            for server in server_sort_by_hardware_cost:
                if server["server_cpu_num"] / denominator >= vm["vm_cpu_num"] and server["server_memory_num"] / denominator >= vm["vm_memory_num"]:
                    self.best_server_for_vm["{}".format(vm["vm_name"])] = server


    def purchase(self, purchase_list):
        """
        购买服务器
        :param purchase_list: 购买列表。类型为 [(server_type_dict, num)]
        """
        print("(purchase, {})".format(len(purchase_list)))

        for server in purchase_list:
            print("({}, {})".format(server[0]["server_name"], server[1]))

            for i in range(server[1]):
                self.server_list.append(self.server_id)
                self.idle_server_list.append(self.server_id)
                self.server_map[self.server_id] = server[0]
                self.server_id += 1

            for s in self.server_type_list:
                if s["server_name"] == server[0]:
                    self.cost += s["server_hardware_cost"]

    def migration(self, migration_list):
        """
        迁移服务器
        将第一个参数代表的服务器迁移到第二个参数代表的服务器
        :param migration_list: 迁移列表。类型为 [vm_id, server_id] 或 [vm_id, server_id, partition]
        """
        print("(migration, {})".format(len(migration_list)))

        for migration in migration_list:
            if len(migration) == 3:
                print("({}, {}, {})".format(migration[0], migration[1], migration[2]))
            else:
                print("({}, {})".format(migration[0], migration[1]))

    def create(self, create_list):
        """
        创建虚拟机
        :param create_list:创建列表。类型为 [server_id, partition] 或 [server_id]
        """
        for create in create_list:
            if len(create) == 2:
                print("({}, {})".format(create[0], create[1]))
            else:
                print("({})".format(create[0]))

    def delete(self, delete_list):
        """
        删除虚拟机
        :param delete_list:删除列表。类型为 []
        """

    def get_cost(self):
        """
        返回总花费
        :return: 总花费
        """
        return self.cost


def algorithm01():
    algorithm_result = algorithm()
    return algorithm_result.get_cost()


def get_result():
    cost = algorithm01()
    print(cost)


if __name__ == "__main__":
    get_result()
