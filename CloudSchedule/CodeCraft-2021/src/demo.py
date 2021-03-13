import read_file


class Algorithm(object):

    def __init__(self):
        training_data = read_file.get_training_data()
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()

        # cpu密集或者memory密集的服务器类型
        self.server_type_list_more_cpu = []
        self.server_type_list_equal = []
        self.server_type_list_more_memory = []
        self.server_type_list_triple()

        # 存储单节点虚拟机的服务器
        self.server_single_more_cpu = {}
        self.server_single_equal = {}
        self.server_single_more_memory = {}
        # 存储双节点虚拟机的服务器
        self.server_double_more_cpu = {}
        self.server_double_equal = {}
        self.server_double_more_memory = {}

        self.add_request_single_more_cpu = []
        self.add_request_single_equal = []
        self.add_request_single_more_memory = []
        self.add_request_double_more_cpu = []
        self.add_request_double_equal = []
        self.add_request_double_more_memory = []
        self.del_request = []

        # 总支出
        self.cost = 0
        # 当前 server_id
        self.server_id = 0
        # 虚拟机ID：所在服务器ID键值对
        self.vm_id_to_server_id = {}

        for day in range(self.daily_num):
            daily_queue = self.daily_queue_list[day]
            self.process_daily_queue(daily_queue, day)

    def process_daily_queue(self, daily_queue, day):
        request_id = 0
        for request in daily_queue.get_daily_queue_info():
            request.update({"request_id": request_id})
            request_id += 1
            if request["request_item_action"] == "add":
                for vm in self.vm_type_list:
                    if vm["vm_name"] == request["request_item_vm_type"]:
                        if vm["vm_deployment_way"] == 0 and abs(vm["vm_cpu_num"] - vm["vm_memory_size"]) < 20:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_single_equal.append(request)
                        elif vm["vm_deployment_way"] == 0 and vm["vm_cpu_num"] > vm["vm_memory_size"]:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_single_more_cpu.append(request)
                        elif vm["vm_deployment_way"] == 0 and vm["vm_cpu_num"] < vm["vm_memory_size"]:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_single_more_memory.append(request)
                        elif vm["vm_deployment_way"] == 1 and abs(vm["vm_cpu_num"] - vm["vm_memory_size"]) < 20:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_double_equal.append(request)
                        elif vm["vm_deployment_way"] == 1 and vm["vm_cpu_num"] > vm["vm_memory_size"]:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_double_more_cpu.append(request)
                        elif vm["vm_deployment_way"] == 1 and vm["vm_cpu_num"] < vm["vm_memory_size"]:
                            request.update({"cpu_num": vm["vm_cpu_num"], "memory_size": vm["vm_memory_size"]})
                            self.add_request_double_more_memory.append(request)
                    else:
                        continue
            else:
                self.del_request.append(request)

        # 处理请求的第一阶段，利用旧的服务器来满足新的虚拟机创建请求
        self.add_request_single_more_cpu, self.server_single_more_cpu, sc = \
            self.process_single_via_old_server(self.add_request_single_more_cpu, self.server_single_more_cpu)
        self.add_request_single_equal, self.server_single_equal, se = \
            self.process_single_via_old_server(self.add_request_single_equal, self.server_single_equal)
        self.add_request_single_more_memory, self.server_single_more_memory, sm = \
            self.process_single_via_old_server(self.add_request_single_more_memory, self.server_single_more_memory)
        self.add_request_double_more_cpu, self.server_double_more_cpu, dc = \
            self.process_double_via_old_server(self.add_request_double_more_cpu, self.server_double_more_cpu)
        self.add_request_double_equal, self.server_double_equal, de = \
            self.process_double_via_old_server(self.add_request_double_equal, self.server_double_equal)
        self.add_request_double_more_memory, self.server_double_more_memory, dm = \
            self.process_double_via_old_server(self.add_request_double_more_memory, self.server_double_more_memory)

        step_1_decision = sc + se + sm + dc + de + dm

        # 处理请求的第二阶段，继续处理第一阶段处理完之后剩下的请求，这就需要购买新的服务器

        self.add_request_single_more_cpu = sorted(self.add_request_single_more_cpu,
                                                  key=lambda x: x["cpu_num"])
        self.add_request_single_equal = sorted(self.add_request_single_equal,
                                               key=lambda x: x["cpu_num"] + x["memory_size"])
        self.add_request_single_more_memory = sorted(self.add_request_single_more_memory,
                                                     key=lambda x: x["memory_size"])
        self.add_request_double_more_cpu = sorted(self.add_request_double_more_cpu,
                                                  key=lambda x: x["cpu_num"])
        self.add_request_double_equal = sorted(self.add_request_double_equal,
                                               key=lambda x: x["cpu_num"] + x["memory_size"])
        self.add_request_double_more_memory = sorted(self.add_request_double_more_memory,
                                                     key=lambda x: x["memory_size"])

        ps_sc, sc = self.single_more_cpu_purchase(day)
        ps_se, se = self.single_equal_purchase(day)
        ps_sm, sm = self.single_more_memory_purchase(day)
        ps_dc, dc = self.double_more_cpu_purchase(day)
        ps_de, de = self.double_equal_purchase(day)
        ps_dm, dm = self.double_more_memory_purchase(day)

        purchase_server = ps_sc + ps_se + ps_sm + ps_dc + ps_de + ps_dm
        step_2_decision = sc + se + sm + dc + de + dm

        # 处理请求的第三阶段，即删除操作
        self.delete()

        # 迁移阶段

        # 输出阶段
        print("(purchase, {})".format(len(purchase_server)))

        purchase_server = sorted(purchase_server, key=lambda x: x[0])
        for purchase in purchase_server:
            print("({}, {})".format(purchase[1], 1))

        print("({}, {})".format("migration", "0"))

        all_decision = step_1_decision + step_2_decision
        sorted_decision = sorted(all_decision, key=lambda x: x[0])
        for decision in sorted_decision:
            print("{}".format(decision[1]))

    def single_more_cpu_purchase(self, day):
        index = 0
        purchase_sc_server = []
        decision = []
        server_sort_by_cpu = sorted(self.server_type_list_more_cpu, key=lambda x: x["server_cpu_num"])
        while index < len(self.add_request_single_more_cpu):
            if index < len(self.add_request_single_more_cpu) - 1:
                cpu_num = self.add_request_single_more_cpu[index + 1]["cpu_num"]
                for server in server_sort_by_cpu:
                    if server["server_cpu_num"] / 2 >= cpu_num and \
                            server["server_memory_size"] / 2 >= self.add_request_single_more_cpu[index][
                        "memory_size"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_more_cpu[index + 1][
                        "memory_size"]:
                        purchase_sc_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"date": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_more_cpu[index]["request_item_vm_id"],
                                             self.add_request_single_more_cpu[index]["cpu_num"],
                                             self.add_request_single_more_cpu[index]["memory_size"],
                                             "A"],
                                            [self.add_request_single_more_cpu[index + 1]["request_item_vm_id"],
                                             self.add_request_single_more_cpu[index + 1]["cpu_num"],
                                             self.add_request_single_more_cpu[index + 1]["memory_size"],
                                             "B"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_cpu[index]["cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_cpu[index][
                                     "memory_size"],
                             "B_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_cpu[index + 1][
                                     "cpu_num"],
                             "B_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_cpu[index + 1][
                                     "memory_size"]})
                        decision.append(
                            [self.add_request_single_more_cpu[index]["request_id"], (self.server_id, "A")])
                        decision.append(
                            [self.add_request_single_more_cpu[index + 1]["request_id"], (self.server_id, "B")])
                        self.vm_id_to_server_id.update({self.add_request_single_more_cpu[index]["request_item_vm_id"]:
                                                            self.server_id})
                        self.vm_id_to_server_id.update(
                            {self.add_request_single_more_cpu[index + 1]["request_item_vm_id"]:
                                 self.server_id})
                        self.server_single_more_cpu.update({self.server_id: server})
                        self.server_id += 1
                        index += 2
                        break
                    else:
                        continue
            else:
                for server in server_sort_by_cpu:
                    if server["server_cpu_num"] / 2 >= self.add_request_single_more_cpu[index]["cpu_num"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_more_cpu[index]["memory_size"]:
                        purchase_sc_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"day": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_more_cpu[index]["request_item_vm_id"],
                                             self.add_request_single_more_cpu[index]["cpu_num"],
                                             self.add_request_single_more_cpu[index]["memory_size"],
                                             "A"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_cpu[index]["cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_cpu[index][
                                     "memory_size"],
                             "B_rest_cpu_num": server["server_cpu_num"] / 2,
                             "B_rest_memory_size": server["server_memory_size"] / 2})
                        decision.append(
                            [self.add_request_single_more_cpu[index]["request_id"], (self.server_id, "A")])
                        self.vm_id_to_server_id.update({self.add_request_single_more_cpu[index]["request_item_vm_id"]:
                                                            self.server_id})
                        self.server_single_more_cpu.update({self.server_id: server})
                        self.server_id += 1
                        index += 1
                        break
                    else:
                        continue
        self.add_request_single_more_cpu.clear()
        return purchase_sc_server, decision

    def single_equal_purchase(self, day):
        index = 0
        purchase_se_server = []
        decision = []
        server_sort_by_cpu_memory = sorted(self.server_type_list_equal,
                                           key=lambda x: x["server_cpu_num"] + x["server_memory_size"])
        while index < len(self.add_request_single_equal):
            if index < len(self.add_request_single_equal) - 1:
                for server in server_sort_by_cpu_memory:
                    if server["server_cpu_num"] / 2 >= self.add_request_single_equal[index]["cpu_num"] and \
                            server["server_cpu_num"] / 2 >= self.add_request_single_equal[index + 1]["cpu_num"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_equal[index][
                        "memory_size"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_equal[index + 1][
                        "memory_size"]:
                        purchase_se_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"day": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_equal[index]["request_item_vm_id"],
                                             self.add_request_single_equal[index]["cpu_num"],
                                             self.add_request_single_equal[index]["memory_size"],
                                             "A"],
                                            [self.add_request_single_equal[index + 1]["request_item_vm_id"],
                                             self.add_request_single_equal[index + 1]["cpu_num"],
                                             self.add_request_single_equal[index + 1]["memory_size"],
                                             "B"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_equal[index]["cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_equal[index][
                                     "memory_size"],
                             "B_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_equal[index + 1]["cpu_num"],
                             "B_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_equal[index + 1][
                                     "memory_size"]})
                        decision.append(
                            [self.add_request_single_equal[index]["request_id"], (self.server_id, "A")])
                        decision.append(
                            [self.add_request_single_equal[index + 1]["request_id"], (self.server_id, "B")])
                        self.vm_id_to_server_id.update({self.add_request_single_equal[index]["request_item_vm_id"]:
                                                            self.server_id})
                        self.vm_id_to_server_id.update({self.add_request_single_equal[index + 1]["request_item_vm_id"]:
                                                            self.server_id})
                        self.server_single_equal.update({self.server_id: server})
                        self.server_id += 1

                        index += 2
                        break
                    else:
                        continue
            else:
                for server in server_sort_by_cpu_memory:
                    if server["server_cpu_num"] / 2 >= self.add_request_single_equal[index]["cpu_num"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_equal[index]["memory_size"]:
                        purchase_se_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"day": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_equal[index]["request_item_vm_id"],
                                             self.add_request_single_equal[index]["cpu_num"],
                                             self.add_request_single_equal[index]["memory_size"],
                                             "A"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_equal[index]["cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_equal[index][
                                     "memory_size"],
                             "B_rest_cpu_num": server["server_cpu_num"] / 2,
                             "B_rest_memory_size": server["server_memory_size"] / 2})
                        decision.append(
                            [self.add_request_single_equal[index]["request_id"], (self.server_id, "A")])
                        self.vm_id_to_server_id.update({self.add_request_single_equal[index]["request_item_vm_id"]:
                                                            self.server_id})
                        self.server_single_equal.update({self.server_id: server})
                        self.server_id += 1
                        index += 1
                        break
                    else:
                        continue
        self.add_request_single_equal.clear()
        return purchase_se_server, decision

    def single_more_memory_purchase(self, day):
        index = 0
        purchase_sm_server = []
        decision = []
        server_sort_by_memory = sorted(self.server_type_list_more_memory, key=lambda x: x["server_memory_size"])
        while index < len(self.add_request_single_more_memory):
            if index < len(self.add_request_single_more_memory) - 1:
                memory_size = self.add_request_single_more_memory[index + 1]["memory_size"]
                for server in server_sort_by_memory:
                    if server["server_memory_size"] / 2 >= memory_size and \
                            server["server_cpu_num"] / 2 >= self.add_request_single_more_memory[index][
                        "cpu_num"] and \
                            server["server_cpu_num"] / 2 >= self.add_request_single_more_memory[index + 1][
                        "cpu_num"]:
                        purchase_sm_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"day": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_more_memory[index]["request_item_vm_id"],
                                             self.add_request_single_more_memory[index]["cpu_num"],
                                             self.add_request_single_more_memory[index]["memory_size"],
                                             "A"],
                                            [self.add_request_single_more_memory[index + 1]["request_item_vm_id"],
                                             self.add_request_single_more_memory[index + 1]["cpu_num"],
                                             self.add_request_single_more_memory[index + 1]["memory_size"],
                                             "B"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_memory[index][
                                     "cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_memory[index][
                                     "memory_size"],
                             "B_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_memory[index + 1][
                                     "cpu_num"],
                             "B_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_memory[index + 1][
                                     "memory_size"]})
                        decision.append(
                            [self.add_request_single_more_memory[index]["request_id"], (self.server_id, "A")])
                        decision.append(
                            [self.add_request_single_more_memory[index + 1]["request_id"], (self.server_id, "B")])
                        self.vm_id_to_server_id.update(
                            {self.add_request_single_more_memory[index]["request_item_vm_id"]:
                                 self.server_id})
                        self.vm_id_to_server_id.update(
                            {self.add_request_single_more_memory[index + 1]["request_item_vm_id"]:
                                 self.server_id})
                        self.server_single_more_memory.update({self.server_id: server})
                        self.server_id += 1
                        index += 2
                        break
                    else:
                        continue
            else:
                for server in server_sort_by_memory:
                    if server["server_cpu_num"] / 2 >= self.add_request_single_more_memory[index]["cpu_num"] and \
                            server["server_memory_size"] / 2 >= self.add_request_single_more_memory[index][
                        "memory_size"]:
                        purchase_sm_server.append([self.server_id, server["server_name"]])
                        server.update(
                            {"day": day,
                             "already_cost": server["server_hardware_cost"],
                             "vm_include": [[self.add_request_single_more_memory[index]["request_item_vm_id"],
                                             self.add_request_single_more_memory[index]["cpu_num"],
                                             self.add_request_single_more_memory[index]["memory_size"],
                                             "A"]],
                             "A_rest_cpu_num":
                                 server["server_cpu_num"] / 2 - self.add_request_single_more_memory[index][
                                     "cpu_num"],
                             "A_rest_memory_size":
                                 server["server_memory_size"] / 2 - self.add_request_single_more_memory[index][
                                     "memory_size"],
                             "B_rest_cpu_num": server["server_cpu_num"] / 2,
                             "B_rest_memory_size": server["server_memory_size"] / 2})
                        decision.append(
                            [self.add_request_single_more_memory[index]["request_id"], (self.server_id, "A")])
                        self.vm_id_to_server_id.update(
                            {self.add_request_single_more_memory[index]["request_item_vm_id"]:
                                 self.server_id})
                        self.server_single_more_memory.update({self.server_id: server})
                        self.server_id += 1
                        index += 1
                        break
                    else:
                        continue
        self.add_request_single_more_memory.clear()
        return purchase_sm_server, decision

    def double_more_cpu_purchase(self, day):
        purchase_dc_server = []
        decision = []
        server_sort_by_cpu = sorted(self.server_type_list_more_cpu, key=lambda x: x["server_cpu_num"])
        for request in self.add_request_double_more_cpu:
            for server in server_sort_by_cpu:
                if server["server_cpu_num"] >= request["cpu_num"] and \
                        server["server_memory_size"] >= request["memory_size"]:
                    purchase_dc_server.append([self.server_id, server["server_name"]])
                    server.update(
                        {"day": day,
                         "already_cost": server["server_hardware_cost"],
                         "vm_include": [[request["request_item_vm_id"],
                                         request["cpu_num"],
                                         request["memory_size"],
                                         "AB"]],
                         "A_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "A_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2,
                         "B_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "B_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2
                         }
                    )
                    decision.append([request["request_id"], "(" + str(self.server_id) + ")"])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: self.server_id})
                    self.server_double_more_cpu.update({self.server_id: server})
                    self.server_id += 1
                    break
                else:
                    continue
        self.add_request_double_more_cpu.clear()
        return purchase_dc_server, decision

    def double_equal_purchase(self, day):
        purchase_de_server = []
        decision = []
        server_sort_by_cpu_memory = sorted(self.server_type_list_equal,
                                           key=lambda x: x["server_cpu_num"] + x["server_memory_size"])
        for request in self.add_request_double_equal:
            for server in server_sort_by_cpu_memory:
                if server["server_cpu_num"] >= request["cpu_num"] and \
                        server["server_memory_size"] >= request["memory_size"]:
                    purchase_de_server.append([self.server_id, server["server_name"]])
                    server.update(
                        {"day": day,
                         "already_cost": server["server_hardware_cost"],
                         "vm_include": [[request["request_item_vm_id"],
                                         request["cpu_num"],
                                         request["memory_size"],
                                         "AB"]],
                         "A_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "A_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2,
                         "B_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "B_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2
                         }
                    )
                    decision.append([request["request_id"], "(" + str(self.server_id) + ")"])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: self.server_id})
                    self.server_double_equal.update({self.server_id: server})
                    self.server_id += 1
                    break
                else:
                    continue
        self.add_request_double_equal.clear()
        return purchase_de_server, decision

    def double_more_memory_purchase(self, day):
        purchase_dm_server = []
        decision = []
        server_sort_by_memory = sorted(self.server_type_list_more_memory, key=lambda x: x["server_memory_size"])
        for request in self.add_request_double_more_memory:
            for server in server_sort_by_memory:
                if server["server_cpu_num"] >= request["cpu_num"] and \
                        server["server_memory_size"] >= request["memory_size"]:
                    purchase_dm_server.append([self.server_id, server["server_name"]])
                    server.update(
                        {"day": day,
                         "already_cost": server["server_hardware_cost"],
                         "vm_include": [[request["request_item_vm_id"],
                                         request["cpu_num"],
                                         request["memory_size"],
                                         "AB"]],
                         "A_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "A_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2,
                         "B_rest_cpu_num": server["server_cpu_num"] / 2 - request["cpu_num"] / 2,
                         "B_rest_memory_size": server["server_memory_size"] / 2 - request["memory_size"] / 2
                         }
                    )
                    decision.append([request["request_id"], "(" + str(self.server_id) + ")"])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: self.server_id})
                    self.server_double_more_memory.update({self.server_id: server})
                    self.server_id += 1
                    break
                else:
                    continue
        self.add_request_double_more_memory.clear()
        return purchase_dm_server, decision

    def process_single_via_old_server(self, request_list, server_dict):
        decision = []
        to_del = []
        for request in request_list:
            for server_id, server in server_dict.items():
                if request["cpu_num"] <= server["A_rest_cpu_num"] and \
                        request["memory_size"] <= server["A_rest_memory_size"]:
                    server["A_rest_cpu_num"] -= request["cpu_num"]
                    server["A_rest_memory_size"] -= request["memory_size"]
                    server["vm_include"] += [[request["request_item_vm_id"],
                                              request["cpu_num"],
                                              request["memory_size"],
                                              "A"]]
                    decision.append([request["request_id"], (server_id, "A")])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: server_id})
                    to_del.append(request)
                    break
                elif request["cpu_num"] <= server["B_rest_cpu_num"] and \
                        request["memory_size"] <= server["B_rest_memory_size"]:
                    server["B_rest_cpu_num"] -= request["cpu_num"]
                    server["B_rest_memory_size"] -= request["memory_size"]
                    server["vm_include"] += [[request["request_item_vm_id"],
                                              request["cpu_num"],
                                              request["memory_size"],
                                              "B"]]
                    decision.append([request["request_id"], (server_id, "B")])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: server_id})
                    to_del.append(request)
                    break
                else:
                    continue
        for request in to_del:
            request_list.remove(request)
        return request_list, server_dict, decision

    def process_double_via_old_server(self, request_list, server_dict):
        decision = []
        to_del = []
        for request in request_list:
            for server_id, server in server_dict.items():
                if request["cpu_num"] / 2 <= server["A_rest_cpu_num"] and \
                        request["memory_size"] / 2 <= server["A_rest_memory_size"]:
                    server["A_rest_cpu_num"] -= request["cpu_num"] / 2
                    server["A_rest_memory_size"] -= request["memory_size"] / 2
                    server["B_rest_cpu_num"] -= request["cpu_num"] / 2
                    server["B_rest_memory_size"] -= request["memory_size"] / 2
                    server["vm_include"] += [[request["request_item_vm_id"],
                                              request["cpu_num"],
                                              request["memory_size"],
                                              "AB"]]
                    decision.append([request["request_id"], "(" + str(server_id) + ")"])
                    self.vm_id_to_server_id.update({request["request_item_vm_id"]: server_id})
                    to_del.append(request)
                    break
                else:
                    continue
        for request in to_del:
            request_list.remove(request)
        return request_list, server_dict, decision

    def delete(self):
        for request in self.del_request:
            del_vm_id = request["request_item_vm_id"]
            del_server_id = self.vm_id_to_server_id[del_vm_id]
            if del_server_id in self.server_single_more_cpu.keys():
                for del_vm in self.server_single_more_cpu[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        if del_vm[3] == "A":
                            self.server_single_more_cpu[del_server_id]["A_rest_cpu_num"] += del_vm[1]
                            self.server_single_more_cpu[del_server_id]["A_rest_memory_size"] += del_vm[2]
                        else:
                            self.server_single_more_cpu[del_server_id]["B_rest_cpu_num"] += del_vm[1]
                            self.server_single_more_cpu[del_server_id]["B_rest_memory_size"] += del_vm[2]
                        self.server_single_more_cpu[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue
            elif del_server_id in self.server_single_equal.keys():
                for del_vm in self.server_single_equal[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        if del_vm[3] == "A":
                            self.server_single_equal[del_server_id]["A_rest_cpu_num"] += del_vm[1]
                            self.server_single_equal[del_server_id]["A_rest_memory_size"] += del_vm[2]
                        else:
                            self.server_single_equal[del_server_id]["B_rest_cpu_num"] += del_vm[1]
                            self.server_single_equal[del_server_id]["B_rest_memory_size"] += del_vm[2]
                        self.server_single_equal[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue
            elif del_server_id in self.server_single_more_memory.keys():
                for del_vm in self.server_single_more_memory[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        if del_vm[3] == "A":
                            self.server_single_more_memory[del_server_id]["A_rest_cpu_num"] += del_vm[1]
                            self.server_single_more_memory[del_server_id]["A_rest_memory_size"] += del_vm[2]
                        else:
                            self.server_single_more_memory[del_server_id]["B_rest_cpu_num"] += del_vm[1]
                            self.server_single_more_memory[del_server_id]["B_rest_memory_size"] += del_vm[2]
                        self.server_single_more_memory[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue
            elif del_server_id in self.server_double_more_cpu.keys():
                for del_vm in self.server_double_more_cpu[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        self.server_double_more_cpu[del_server_id]["A_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_more_cpu[del_server_id]["A_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_more_cpu[del_server_id]["B_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_more_cpu[del_server_id]["B_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_more_cpu[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue
            elif del_server_id in self.server_double_equal.keys():
                for del_vm in self.server_double_equal[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        self.server_double_equal[del_server_id]["A_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_equal[del_server_id]["A_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_equal[del_server_id]["B_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_equal[del_server_id]["B_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_equal[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue

            elif del_server_id in self.server_double_more_memory.keys():
                for del_vm in self.server_double_more_memory[del_server_id]["vm_include"]:
                    if del_vm_id == del_vm[0]:
                        self.server_double_more_memory[del_server_id]["A_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_more_memory[del_server_id]["A_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_more_memory[del_server_id]["B_rest_cpu_num"] += del_vm[1] / 2
                        self.server_double_more_memory[del_server_id]["B_rest_memory_size"] += del_vm[2] / 2
                        self.server_double_more_memory[del_server_id]["vm_include"].remove(del_vm)
                        break
                    else:
                        continue
            else:
                print("ERROR!")

    def get_cost(self):
        for server_dict in [self.server_single_more_cpu, self.server_single_equal, self.server_single_more_memory,
                            self.server_double_more_cpu, self.server_double_equal, self.server_double_more_memory]:
            for server_id, server in server_dict.items():
                self.cost += server["server_hardware_cost"] + server["day"] * server["server_energy_cost"]
        return self.cost

    def server_type_list_triple(self):
        for server in self.server_type_list:
            if abs(server["server_cpu_num"] - server["server_memory_size"]) < 200:
                self.server_type_list_equal.append(server)
            elif server["server_cpu_num"] > server["server_memory_size"]:
                self.server_type_list_more_cpu.append(server)
            else:
                self.server_type_list_more_memory.append(server)


def algorithm_demo():
    algorithm_result = Algorithm()
    return algorithm_result.get_cost()


if __name__ == "__main__":
    cost = algorithm_demo()
    print(cost)
