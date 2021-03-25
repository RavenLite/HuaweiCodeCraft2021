package utils;

import pojo.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Read {

    public TrainingData read() {
        Scanner in = new Scanner(System.in);

        int server_type_num = Integer.parseInt(in.nextLine());
        ArrayList<ServerType> server_type_list = new ArrayList<>();
        for (int i = 0; i < server_type_num; ++i) {
            String[] stringList = in.nextLine().replace("(", "").
                    replace(")", "").split(", ");
            String serverTypeName = stringList[0];
            int serverTypeCpuNum = Integer.parseInt(stringList[1]);
            int serverTypeMemoryNum = Integer.parseInt(stringList[2]);
            int serverTypeHardwareCost = Integer.parseInt(stringList[3]);
            int serverTypeRunningCost = Integer.parseInt(stringList[4]);
            ServerType server_type = new ServerType(serverTypeName, serverTypeCpuNum,
                    serverTypeMemoryNum, serverTypeHardwareCost, serverTypeRunningCost);
            server_type_list.add(server_type);
        }

        // 读取 vm_type_num 及 vm_type_list
        int vm_type_num = Integer.parseInt(in.nextLine());
        ArrayList<VmType> vm_type_list = new ArrayList<>();
        for (int i = 0; i < vm_type_num; ++i) {
            String[] stringList = in.nextLine().replace("(", "").
                    replace(")", "").split(", ");
            String vmTypeName = stringList[0];
            int vmTypeCpuNum = Integer.parseInt(stringList[1]);
            int vmTypeMemoryNum = Integer.parseInt(stringList[2]);
            int vmTypeDeploymentWay = Integer.parseInt(stringList[3]);
            VmType vm_type = new VmType(vmTypeName, vmTypeCpuNum, vmTypeMemoryNum, vmTypeDeploymentWay);
            vm_type_list.add(vm_type);
        }

        // 构建 server_type_map 及 vm_type_map
        HashMap<String, ServerType> server_type_map = new HashMap<>();
        for (ServerType st : server_type_list) {
            server_type_map.put(st.getServerTypeName(), st);
        }
        HashMap<String, VmType> vm_type_map = new HashMap<>();
        for (VmType vt : vm_type_list) {
            vm_type_map.put(vt.getVmTypeName(), vt);
        }

        // 读取 daily_queue_num 及 daily_queue_list
        int daily_queue_num = Integer.parseInt(in.nextLine());
        ArrayList<DailyQueue> daily_queue_list = new ArrayList<>();
        for (int i = 0; i < daily_queue_num; ++i) {
            int queue_item_num = Integer.parseInt(in.nextLine());
            ArrayList<QueueItem> queue_item_list = new ArrayList<>();
            for (int j = 0; j < queue_item_num; ++j) {
                String[] stringList = in.nextLine().replace("(", "").
                        replace(")", "").split(", ");
                String queueItemAction = stringList[0];
                VmType queueItemVmType;
                int queueItemVmId;
                if (queueItemAction.equals("add")) {
                    queueItemVmType = vm_type_map.get(stringList[1]);
                    queueItemVmId = Integer.parseInt(stringList[2]);
                } else {
                    queueItemVmType = null;
                    queueItemVmId = Integer.parseInt(stringList[1]);
                }
                QueueItem queue_item = new QueueItem(queueItemAction, queueItemVmType, queueItemVmId);
                queue_item_list.add(queue_item);
            }
            DailyQueue daily_queue = new DailyQueue(queue_item_num, queue_item_list);
            daily_queue_list.add(daily_queue);
        }

        // 进行测试
        test(server_type_list, vm_type_list, daily_queue_list);

        // 返回 training_data
        return new TrainingData(server_type_num, server_type_map, server_type_list,
                vm_type_num, vm_type_map, vm_type_list, daily_queue_num, daily_queue_list);
    }


    public void test(ArrayList<ServerType> server_type_list, ArrayList<VmType> vm_type_list,
                     ArrayList<DailyQueue> daily_queue_list) {
//        System.out.println(server_type_list.size());
//        System.out.println(vm_type_list.size());
//        System.out.println(daily_queue_list.size());
    }
}
