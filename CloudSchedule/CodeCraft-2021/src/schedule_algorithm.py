import glog

import read_file
import constant
import output


# 数据中心资源池，用于管理当前数据中心拥有的资源
class ResourcePool(object):

    def __init__(self):
        # 数据中心拥有的 server 列表（含虚拟服务器）
        self.server_list = []
        # 数据中心拥有的 vm 列表
        self.vm_list = []

        # vm 归属的 server_id
        self.vm_server_id_dict = {}

        # 拥有的真实 Server 数量
        self.real_server_count = constant.ZERO_NUM

        # 加快请求速度，根据 type_name 构建字典, Static
        self.server_type_dict = {}
        self.vm_type_dict = {}


# TODO: 优化该算法以便取得更好的调度结果
def calculate_weight(ratio_cpu_num_left, ratio_memory_size_left, value_ratio, value_cost):
    return ratio_cpu_num_left * 10 + ratio_memory_size_left * 10 + value_ratio * 10 + value_cost / 20000


class Algorithm(object):
    def __init__(self):
        training_data = read_file.get_training_data()

        # read basic fields | 读入基本输入数据
        self.server_type_num = training_data.server_type_num
        self.server_type_list = training_data.server_type_list
        self.vm_type_num = training_data.vm_type_num
        self.vm_type_list = training_data.vm_type_list
        self.daily_num = training_data.daily_queue_num
        self.daily_queue_list = training_data.daily_queue_list

        # initialize assisted fields | 初始化辅助变量
        self.resource_pool = ResourcePool()
        self.server_daily_count = constant.ZERO_NUM

    # 处理每一天的请求队列
    def process_period_queue(self):
        self.before_process_period_queue()
        for index, daily_queue in enumerate(self.daily_queue_list):
            glog.info("Running: {}/{}, ServerCount: {}".format(index, self.daily_num, len(self.resource_pool.server_list)))
            self.process_daily_queue(daily_queue)

    # 处理当天的请求队列
    def process_daily_queue(self, daily_queue):
        old_new_server_id_dict = {}

        self.before_process_daily_queue()

        for queue_item in daily_queue.queue_item_list:
            self.process_queue_item(queue_item)

        self.after_process_daily_queue(daily_queue, old_new_server_id_dict)

    # 处理当天的每一条请求
    def process_queue_item(self, queue_item):
        if queue_item.queue_item_action == constant.ACTION_ADD:
            self.process_queue_item_add(queue_item)
        else:
            self.process_queue_item_del(queue_item)

    # 处理添加请求
    def process_queue_item_add(self, queue_item):
        # 初始化临时最优变量
        best_server = None
        min_value = constant.MIN_VALUE_INITIAL
        temp_value_cpu_num_left = constant.ZERO_NUM
        temp_value_memory_size_left = constant.ZERO_NUM
        temp_value_cpu_num_left_a = constant.ZERO_NUM
        temp_value_cpu_num_left_b = constant.ZERO_NUM
        temp_value_memory_size_left_a = constant.ZERO_NUM
        temp_value_memory_size_left_b = constant.ZERO_NUM
        # 记录剩余值
        value_cpu_num_left_a = constant.ZERO_NUM
        value_cpu_num_left_b = constant.ZERO_NUM
        value_memory_size_left_a = constant.ZERO_NUM
        value_memory_size_left_b = constant.ZERO_NUM

        temp_node = constant.NULL_STRING
        # 解析请求需求
        queue_item_vm_type = self.resource_pool.vm_type_dict[queue_item.queue_item_vm_type_name]

        for server in self.resource_pool.server_list:
            # 指标 1，2: cpu，memory
            # 单节点部署
            if queue_item_vm_type.vm_type_deployment_way == constant.VM_DEPLOYMENT_SINGLE:
                # 剩余不足直接跳过
                if (server.server_cpu_num_left_a < queue_item_vm_type.vm_type_cpu_num
                    and server.server_cpu_num_left_b < queue_item_vm_type.vm_type_cpu_num) \
                        or (server.server_memory_size_left_a < queue_item_vm_type.vm_type_memory_size
                            and server.server_memory_size_left_b < queue_item_vm_type.vm_type_memory_size):
                    continue

                # 判断部署节点，优先部署 A 节点
                server_node = constant.VM_NODE_A \
                    if server.server_cpu_num_left_a > queue_item_vm_type.vm_type_cpu_num and server.\
                    server_memory_size_left_a > queue_item_vm_type.vm_type_memory_size else constant.VM_NODE_B

                # 计算 cpu 剩余 ratio
                value_cpu_num_left = server.server_cpu_num_left_a - queue_item_vm_type.vm_type_cpu_num \
                    if server_node == constant.VM_NODE_A \
                    else server.server_cpu_num_left_b - queue_item_vm_type.vm_type_cpu_num
                ratio_cpu_num_left = value_cpu_num_left / (server.server_type.server_type_cpu_num / 2)

                # 计算 memory 剩余 ratio
                value_memory_size_left = server.server_memory_size_left_a - queue_item_vm_type.vm_type_memory_size \
                    if server_node == constant.VM_NODE_A \
                    else server.server_cpu_num_left_b - queue_item_vm_type.vm_type_memory_size
                ratio_memory_size_left = value_memory_size_left / (server.server_type.server_type_memory_size / 2)
            # 双节点部署
            else:
                # 剩余不足直接跳过
                if server.server_cpu_num_left_a < queue_item_vm_type.vm_type_cpu_num / 2 \
                        or server.server_cpu_num_left_a < queue_item_vm_type.vm_type_cpu_num / 2 \
                        or server.server_memory_size_left_a < queue_item_vm_type.vm_type_memory_size / 2 \
                        or server.server_memory_size_left_b < queue_item_vm_type.vm_type_memory_size / 2:
                    continue
                # 确定部署节点
                server_node = constant.VM_NODE_AB

                # 计算 cpu 剩余 ratio
                value_cpu_num_left = server.server_cpu_num_left_a + server.server_cpu_num_left_b - queue_item_vm_type. \
                    vm_type_cpu_num
                ratio_cpu_num_left = value_cpu_num_left / server.server_type.server_type_cpu_num
                value_cpu_num_left_a = server.server_cpu_num_left_a - queue_item_vm_type.vm_type_cpu_num / 2
                value_cpu_num_left_b = server.server_cpu_num_left_b - queue_item_vm_type.vm_type_cpu_num / 2

                # 计算 memory 剩余 ratio
                value_memory_size_left = server.server_memory_size_left_a + server. \
                    server_memory_size_left_b - queue_item_vm_type.vm_type_memory_size
                ratio_memory_size_left = value_memory_size_left / server.server_type.server_type_memory_size

                value_memory_size_left_a = server.server_cpu_num_left_a - queue_item_vm_type.vm_type_memory_size / 2
                value_memory_size_left_b = server.server_cpu_num_left_b - queue_item_vm_type.vm_type_memory_size / 2

            # 指标 3: ratio
            value_ratio = abs(server.server_type.server_type_ratio - queue_item_vm_type.vm_type_ratio)

            # 指标 4: cost
            # TODO: 考虑运行成本
            value_cost = server.server_type.server_type_hardware_cost

            # 根据权值计算
            server_weight_value = calculate_weight(ratio_cpu_num_left, ratio_memory_size_left, value_ratio, value_cost)

            # 判断是否更优
            if server_weight_value < min_value:
                min_value = server_weight_value
                best_server = server
                temp_value_cpu_num_left = value_cpu_num_left
                temp_value_memory_size_left = value_memory_size_left
                temp_node = server_node

                if server == constant.VM_NODE_AB:
                    temp_value_cpu_num_left_a = value_cpu_num_left_a
                    temp_value_cpu_num_left_b = value_cpu_num_left_b
                    temp_value_memory_size_left_a = value_memory_size_left_a
                    temp_value_memory_size_left_b = value_memory_size_left_b

        # 扣掉 cpu 和 memory
        if temp_node == constant.VM_NODE_A:
            best_server.server_cpu_num_left_a = temp_value_cpu_num_left
            best_server.server_memory_size_left_a = temp_value_memory_size_left
        elif temp_node == constant.VM_NODE_B:
            best_server.server_cpu_num_left_b = temp_value_cpu_num_left
            best_server.server_memory_size_left_b = temp_value_memory_size_left
        else:
            best_server.server_cpu_num_left_a = temp_value_cpu_num_left_a
            best_server.server_memory_size_left_a = temp_value_memory_size_left_a
            best_server.server_cpu_num_left_b = temp_value_cpu_num_left_b
            best_server.server_memory_size_left_b = temp_value_memory_size_left_b

        # 判断是否需要新购买服务器
        if best_server.server_id == constant.VIRTUAL_SERVER_ID:
            # 标记为当天新购买的服务器
            best_server.server_id = constant.NEW_SERVER_ID - self.server_daily_count

            queue_item.server_id = best_server.server_id
            queue_item.server_node = temp_node
            # 购买服务器
            self.purchase_server(best_server.server_type)
        else:
            queue_item.server_id = best_server.server_id
            queue_item.server_node = temp_node

        # 更新 vm-server dict
        self.resource_pool.vm_server_id_dict[queue_item.queue_item_vm_id] = (best_server.server_id, temp_node,
                                                                             queue_item_vm_type.vm_type_cpu_num,
                                                                             queue_item_vm_type.vm_type_memory_size)

    # 购买服务器
    def purchase_server(self, server_type):
        # 添加服务器
        new_server = read_file.Server(server_type)
        self.server_daily_count += 1
        self.resource_pool.server_list.append(new_server)

    # 处理删除请求
    def process_queue_item_del(self, queue_item):
        vm_id = queue_item.queue_item_vm_id
        server_id, server_node, vm_type_cpu_num, vm_type_memory_size = self.resource_pool.vm_server_id_dict[vm_id]
        for server in self.resource_pool.server_list:
            if server.server_id == server_id:
                if server_node == constant.VM_NODE_A:
                    server.server_cpu_num_left_a += vm_type_cpu_num
                    server.server_memory_size_left_a += vm_type_memory_size
                elif server_node == constant.VM_NODE_B:
                    server.server_cpu_num_left_b += vm_type_cpu_num
                    server.server_memory_size_left_b += vm_type_memory_size
                else:
                    server.server_cpu_num_left_a += vm_type_cpu_num / 2
                    server.server_memory_size_left_a += vm_type_memory_size / 2
                    server.server_cpu_num_left_b += vm_type_cpu_num / 2
                    server.server_memory_size_left_b += vm_type_memory_size / 2

    # 处理每一天的请求队列的前置操作
    def before_process_period_queue(self):
        # 分别为 server_type 和 vm_type 构造索引 map
        for server_type in self.server_type_list:
            self.resource_pool.server_type_dict[server_type.server_type_name] = server_type
            # 初始化虚拟服务器
            virtual_server = read_file.Server(server_type)
            self.resource_pool.server_list.append(virtual_server)
        for vm_type in self.vm_type_list:
            self.resource_pool.vm_type_dict[vm_type.vm_type_name] = vm_type

    # 处理当前的请求队列的前置操作
    def before_process_daily_queue(self):
        self.migrate_vm()
        self.server_daily_count = 0

    # 处理当前的请求队列的后置操作
    def after_process_daily_queue(self, daily_queue, old_new_server_id_dict):
        # 为新服务器分配 server_id
        type_count_dict, type_list = self.arrange_server_id(old_new_server_id_dict)
        # 更新使用了新服务器的 item 的 server_id
        for queue_item in daily_queue.queue_item_list:
            if queue_item.queue_item_action == constant.ACTION_ADD and queue_item.server_id <= constant.NEW_SERVER_ID:
                queue_item.server_id = old_new_server_id_dict[queue_item.server_id]

        # output.output_daily(type_count_dict, daily_queue)

    # 迁移资源
    def migrate_vm(self):
        pass

    # 分配服务器ID
    def arrange_server_id(self, old_new_server_id_dict):
        # 服务器类型 - 类型服务器数量
        type_count_dict = {}
        # 服务器类型 - 类型服务器 id 起点
        type_start_dict = {}
        # 服务器类型 - 类型服务器 offset 偏移
        type_offset_dict = {}

        type_list = []

        # 第一次循环，统计类型和数量
        for server in self.resource_pool.server_list:
            if server.server_id <= constant.NEW_SERVER_ID:
                if server.server_type.server_type_name in type_count_dict.keys():
                    type_count_dict[server.server_type.server_type_name] += 1
                else:
                    type_count_dict[server.server_type.server_type_name] = 1

                type_list.append(server.server_type.server_type_name)

        daily_server_count = 0
        for server_type_name in type_count_dict.keys():
            type_start_dict[server_type_name] = daily_server_count + self.resource_pool.real_server_count
            daily_server_count += type_count_dict[server_type_name]
            type_offset_dict[server_type_name] = 0

        # 第二次循环，分配 server id
        for server in self.resource_pool.server_list:
            if server.server_id <= constant.NEW_SERVER_ID:
                server_type_name = server.server_type.server_type_name
                # 计算得到新的 server id
                new_server_id = type_start_dict[server_type_name] + type_offset_dict[server_type_name]
                type_offset_dict[server_type_name] += 1
                # 记录当天临时 server id 与新的 server id 的关系
                old_new_server_id_dict[server.server_id] = new_server_id
                # 赋予 server 以新的 id
                server.server_id = new_server_id

        return type_count_dict, type_list


if __name__ == "__main__":
    Algorithm().process_period_queue()
