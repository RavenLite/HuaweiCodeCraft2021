package utils;

import pojo.*;

import java.util.HashMap;
import java.util.Map;

public class Output {
    private static final Constant constant = new Constant();

    public void output_daily(int purchase_server_num, HashMap<ServerType, Integer> purchase_server_list,
                             int migrate_vm_num, HashMap<Vm, Server> migrate_vm_list,
                             DailyQueue daily_queue_list) {
        System.out.printf("(purchase, %d)%n", purchase_server_num);
        for (Map.Entry<ServerType, Integer> entry : purchase_server_list.entrySet()) {
            System.out.printf("(%s, %d)%n", entry.getKey().getServerTypeName(), entry.getValue());
        }
        System.out.printf("(migration, %d)%n", migrate_vm_num);
//        for (Map.Entry<Vm, Server> entry : migrate_vm_list) {
//            System.out.printf("");
//        }

//        for (QueueItem queue_item : daily_queue_list.getQueueItemList()) {
//            if (queue_item.getQueueItemAction().equals(constant.ACTION_ADD)) {
//                if (queue_item.getQueueItemVmType().getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE) {
//                    System.out.printf("(%d)%n", queue_item.getQueueItemVmType().);
//                } else {
//                    System.out.printf("(%d, %d)%n", );
//                }
//            }
//        }

    }
}
