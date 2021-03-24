package com.huawei.java.main;

import algorithm.ResourcePool;
import algorithm.ScheduleAlgorithm;
import pojo.*;
import utils.Read;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {
    /**
     * 获取 training_data
     * @return training_data
     */
    public static TrainingData get_training_data() {
        try {
            // 构建文件读取器
            BufferedReader in = new BufferedReader(new FileReader("./training_data/training-1.txt"));

            // 读取 server_type_num 及 server_type_list
            int server_type_num = Integer.parseInt(in.readLine());
            ArrayList<ServerType> server_type_list = new ArrayList<>();
            for (int i = 0; i < server_type_num; ++i) {
                String[] stringList = in.readLine().replace("(", "").
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
            int vm_type_num = Integer.parseInt(in.readLine());
            ArrayList<VmType> vm_type_list = new ArrayList<>();
            for (int i = 0; i < vm_type_num; ++i) {
                String[] stringList = in.readLine().replace("(", "").
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
            int daily_queue_num = Integer.parseInt(in.readLine());
            ArrayList<DailyQueue> daily_queue_list = new ArrayList<>();
            for (int i = 0; i < daily_queue_num; ++i) {
                int queue_item_num = Integer.parseInt(in.readLine());
                ArrayList<QueueItem> queue_item_list = new ArrayList<>();
                for (int j = 0; j < queue_item_num; ++j) {
                    String[] stringList = in.readLine().replace("(", "").
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
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 测试类
     * @param server_type_list 服务器类型列表
     * @param vm_type_list 虚拟机类型列表
     * @param daily_queue_list 日常请求列表
     */
    public static void test(ArrayList<ServerType> server_type_list, ArrayList<VmType> vm_type_list,
                            ArrayList<DailyQueue> daily_queue_list) {
//        System.out.println(server_type_list.size());
//        System.out.println(vm_type_list.size());
//        System.out.println(daily_queue_list.size());
    }

    /**
     * 主类
     * @param args 参数
     * @throws FileNotFoundException 缺少文件报错
     */
    public static void main(String[] args) throws FileNotFoundException {
        // TODO: Read standard input
        // TODO: process
        // TODO: write standard Output
        // TODO: System.out.flush()
//        new ScheduleAlgorithm(get_training_data(), new ResourcePool()).processPeriodQueue();
        new ScheduleAlgorithm(new Read().read(), new ResourcePool()).processPeriodQueue();
    }
}