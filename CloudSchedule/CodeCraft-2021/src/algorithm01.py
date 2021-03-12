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
        # 格式：[server_type_dict : vm_type_dict]
        self.server_for_vm = []

        self.process_daily_queue()

    def process_daily_queue(self):
        for daily_queue in self.daily_queue_list:



    def get_best_server_for_vm(self):

        server_sort_by_cpu = sorted(self.server_type_list, key = lambda x : x["server_cpu_num"])
        server_sort_by_memory = sorted(self.server_type_list, key = lambda x : x["server_memory_size"])





    def purchase(self, purchase_list):
        """
        购买服务器
        :param purchase_list: 购买列表。类型为 [(server_name, num)]
        """
        print("(purchase, {})".format(len(purchase_list)))

        for server in purchase_list:
            print("({}, {})".format(server[0], server[1]))

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