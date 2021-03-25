import constant


def output_daily(type_count_dict, daily_queue):
    purchase_type_list = list(type_count_dict.keys())
    purchase_type_count = len(purchase_type_list)
    print("(purchase, {})".format(purchase_type_count))
    for i in range(purchase_type_count):
        print("({}, {})".format(purchase_type_list[i], type_count_dict[purchase_type_list[i]]))
    print("(migration, {})".format(0))
    for queue_item in daily_queue.queue_item_list:
        if queue_item.queue_item_action == constant.ACTION_ADD:
            if queue_item.server_node == constant.VM_NODE_AB:
                print("({})".format(queue_item.server_id))
            else:
                print("({}, {})".format(queue_item.server_id, queue_item.server_node))
