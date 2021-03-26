package utils;

import pojo.*;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * 进行输出
 */
public class OutputFile {

    private static final Constant constant = new Constant();
//    private static int day = 0;

    public static String file_name = "output.txt";

    public static void output_daily(int purchase_server_type_num, HashMap<String, Integer> purchase_server_list,
                             int migrate_vm_num, ArrayList<MigrationItem> dailyMigrationList,
                             DailyQueue daily_queue_list, String fn) {

        file_name = fn;
        try {
            File file = new File(file_name);
            FileOutputStream fos;
            if (!file.exists()) {
                file.createNewFile();
                fos = new FileOutputStream(file);
            } else {
                fos = new FileOutputStream(file, true);
            }
            OutputStreamWriter out = new OutputStreamWriter(fos);
//            System.out.printf("Day: %d%n", day++);

            // 输出购买
            out.write(String.format("(purchase, %d)%n", purchase_server_type_num));
            for (Map.Entry<String, Integer> entry : purchase_server_list.entrySet()) {
                out.write(String.format("(%s, %d)%n", entry.getKey(), entry.getValue()));
            }

            // 输出迁移
//            System.out.printf("%d, %d\n", migrate_vm_num, dailyMigrationList.size());
            out.write(String.format("(migration, %d)%n", migrate_vm_num));
            for (MigrationItem migrationItem : dailyMigrationList) {
                if (migrationItem.getDeploymentNode().equals(constant.VM_NODE_AB)){
                    out.write(String.format("(%d, %d)%n", migrationItem.getVmId(), migrationItem.getServerId()));
                } else {
                    out.write(String.format("(%d, %d, %s)%n", migrationItem.getVmId(), migrationItem.getServerId(), migrationItem.getDeploymentNode()));
                }
            }

            // 输出部署服务器
            for (QueueItem queue_item : daily_queue_list.getQueueItemList()) {
                if (queue_item.getQueueItemAction().equals(constant.ACTION_ADD)) {
                    if (queue_item.getQueueItemVmType().getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE) {
                        out.write(String.format("(%d, %s)%n", queue_item.getQueueVm().getServerId(), queue_item.getQueueVm().getDeployNode()));
                    } else {
                        out.write(String.format("(%d)%n", queue_item.getQueueVm().getServerId()));
                    }
                }
            }
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
