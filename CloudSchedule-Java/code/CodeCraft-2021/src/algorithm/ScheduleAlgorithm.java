package algorithm;

import pojo.*;
import utils.Constant;
import utils.MultipleReturn;
import utils.Output;
import utils.OutputFile;

import java.util.ArrayList;
import java.util.HashMap;


public class ScheduleAlgorithm {
    private TrainingData trainingData;
    private ResourcePool resourcePool;

    private int dailyNewServerCount;
    private static Constant constant = new Constant();

    // 记录了当天购买了新服务器的虚拟机 ID
    private ArrayList<Integer> dailyVmIdOnNewServer = new ArrayList<>();
    private ArrayList<MigrationItem> dailyMigrationList = new ArrayList<>();

    public ScheduleAlgorithm(TrainingData trainingData, ResourcePool resourcePool) {
        this.trainingData = trainingData;
        this.resourcePool = resourcePool;

        this.dailyNewServerCount = 0;
    }

    // 处理周期的请求队列
    public void processPeriodQueue() {
        this.beforeProcessPeriodQueue();

        this.trainingData.getDailyQueueList().forEach(
                dailyQueue -> {
                    // 命令行提示
//                    String str = String.format("Running: %d/%d, ServerCount: %d, DailyQueueSize: %d", this.trainingData.getDailyQueueList().indexOf(dailyQueue) + 1, this.trainingData.getDailyQueueNum(), this.resourcePool.getServerList().size(), dailyQueue.getQueueItemList().size());
//                    System.out.println(str);

                    this.processDailyQueue(dailyQueue);
                }
        );
    }

    // 处理当天的请求队列
    private void processDailyQueue(DailyQueue dailyQueue) {
        this.beforeProcessDailyQueue();

        dailyQueue.getQueueItemList().forEach(
                this::processQueueItem
        );

        this.afterProcessDailyQueue(dailyQueue);
    }

    // 处理当天的每一条请求
    private void processQueueItem(QueueItem queueItem) {
        if (constant.ACTION_ADD.equals(queueItem.getQueueItemAction())) {
            this.processQueueItemAdd(queueItem);
        } else {
            this.processQueueItemDel(queueItem);
        }
    }

    // 处理添加请求
    private void processQueueItemAdd(QueueItem queueItem) {
        VmType queueItemVmType = queueItem.getQueueItemVmType();
        Vm createdVm = this.resourcePool.createVm(queueItem.getQueueItemVmId(), queueItem.getQueueItemVmType());
        queueItem.setQueueVm(createdVm);

        float tempBestServerEvaluation = constant.MIN_VALUE_INITIAL;
        Server tempBestServer = new Server();
        String tempBestDeployNode = null;

        for (Server server : this.resourcePool.getServerList()) {
            // 判断该服务器剩余空间是否满足条件
            if (!this.hasEnoughSpace(queueItem.getQueueItemVmType(), server)) {
                continue;
            }

            // 指标 1, 2: CPU, Memory
            MultipleReturn ratioCpuAndMemoryLeft = this.calculateRatioCpuAndMemoryLeft(queueItemVmType, server);
            float ratioServerCpuNumLeft = ratioCpuAndMemoryLeft.getFirst();
            float ratioServerMemoryNumLeft = ratioCpuAndMemoryLeft.getSecond();
            String deployNode = ratioCpuAndMemoryLeft.getThird();

            // 指标 3: CPU/Memory
            float ratioDensityGap = Math.abs(queueItemVmType.getVmTypeRatioDensity() - server.getServerType().getServerTypeRatioDensity());

            // 指标 4, 5: hardwareCost, runningCost
            float ratioHardwareCost = (float) server.getServerType().getServerTypeHardwareCost();
            float ratioRunningCost = (float) server.getServerType().getServerTypeRunningCost();

            // 评价结果
            float serverEvaluation = this.calculateServerEvaluation(ratioServerCpuNumLeft, ratioServerMemoryNumLeft, ratioDensityGap, ratioHardwareCost, ratioRunningCost);

            if (serverEvaluation < tempBestServerEvaluation) {
                tempBestServerEvaluation = serverEvaluation;
                tempBestServer = server;
                tempBestDeployNode = deployNode;
            }
        }

        // 处理最优情况
        this.handleBetterResult(queueItem, tempBestServer, tempBestDeployNode);
    }

    // 处理最优情况
    private void handleBetterResult(QueueItem queueItem, Server server, String deployNode) {
        server.deployVm(queueItem.getQueueVm(), deployNode);

        // 判断是否需要新购买服务器
        if (server.getServerId() == constant.SERVER_ID_VIRTUAL) {
            // 标记为当天新购买的服务器
            int dailyServerId = constant.SERVER_ID_NEW_START - this.dailyNewServerCount;
            server.setServerId(dailyServerId);

            // 更新虚拟机所属服务器及节点
            queueItem.getQueueVm().setServerId(dailyServerId);
            queueItem.getQueueVm().setDeployNode(deployNode);

            // 购买服务器
            this.resourcePool.buyServer(server);
            this.dailyNewServerCount++;
            this.dailyVmIdOnNewServer.add(queueItem.getQueueItemVmId());
        } else {
            if (server.getServerId() <= constant.SERVER_ID_NEW_START) {
                this.dailyVmIdOnNewServer.add(queueItem.getQueueItemVmId());
            }
            queueItem.getQueueVm().setServerId(server.getServerId());
            queueItem.getQueueVm().setDeployNode(deployNode);
        }

        this.resourcePool.getVmServerMap().put(queueItem.getQueueItemVmId(), server.getServerId());
    }

    // 评价算法
    // TODO: 复杂化
    private float calculateServerEvaluation(float ratioServerCpuNumLeft, float ratioServerMemoryNumLeft, float ratioDensityGap, float ratioHardwareCost, float ratioRunningCost) {
        float serverEvaluation =
                constant.WEIGHT_SERVER_CPU_NUM_LEFT * ratioServerCpuNumLeft * 10
                        + constant.WEIGHT_SERVER_MEMORY_NUM_LEFT * ratioServerMemoryNumLeft * 10
                        + constant.WEIGHT_DENSITY_GAP * ratioDensityGap * 10
                        + constant.WEIGHT_HARDWARE_COST * ratioHardwareCost / 20000
                        + constant.WEIGHT_RUNNING_COST *  ratioRunningCost / 50;
        return serverEvaluation;
    }

    // 迁移的评价算法
    private float calculateServerEvaluationForMigration(float ratioServerCpuNumLeft, float ratioServerMemoryNumLeft, float ratioDensityGap, float ratioHardwareCost, float ratioRunningCost) {
        float serverEvaluation =
                constant.WEIGHT_SERVER_CPU_NUM_LEFT_MIGRATION * ratioServerCpuNumLeft * 10
                        + constant.WEIGHT_SERVER_MEMORY_NUM_LEFT_MIGRATION * ratioServerMemoryNumLeft * 10
                        + constant.WEIGHT_DENSITY_GAP_MIGRATION * ratioDensityGap * 10
                        + constant.WEIGHT_HARDWARE_COST_MIGRATION * ratioHardwareCost / 20000
                        + constant.WEIGHT_RUNNING_COST_MIGRATION *  ratioRunningCost / 50;
        return serverEvaluation;
    }

    private MultipleReturn calculateRatioCpuAndMemoryLeft(VmType queueItemVmType, Server server) {
        int serverCpuNumLeft;
        int serverMemoryNumLeft;
        float ratioServerCpuNumLeft;
        float ratioServerMemoryNumLeft;
        String deployNode = null;

        if (queueItemVmType.getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE) {
            if (server.getServerCpuNumLeftA() >= queueItemVmType.getVmTypeCpuNum() && server.getServerMemoryNumLeftA() >= queueItemVmType.getVmTypeMemoryNum()) {
                serverCpuNumLeft = server.getServerCpuNumLeftA() - queueItemVmType.getVmTypeCpuNum();
                serverMemoryNumLeft = server.getServerMemoryNumLeftA() - queueItemVmType.getVmTypeMemoryNum();
                ratioServerCpuNumLeft = (float) serverCpuNumLeft / (float) (server.getServerType().getServerTypeCpuNum() / 2);
                ratioServerMemoryNumLeft = (float) serverMemoryNumLeft / (float) (server.getServerType().getServerTypeMemoryNum() / 2);

                deployNode = constant.VM_NODE_A;
            } else {
                serverCpuNumLeft = server.getServerCpuNumLeftB() - queueItemVmType.getVmTypeCpuNum();
                serverMemoryNumLeft = server.getServerMemoryNumLeftB() - queueItemVmType.getVmTypeMemoryNum();
                ratioServerCpuNumLeft = (float) serverCpuNumLeft / (float) (server.getServerType().getServerTypeCpuNum() / 2);
                ratioServerMemoryNumLeft = (float) serverMemoryNumLeft / (float) (server.getServerType().getServerTypeMemoryNum() / 2);

                deployNode = constant.VM_NODE_B;
            }
        } else {
            serverCpuNumLeft = server.getServerCpuNumLeftA() + server.getServerCpuNumLeftA() - queueItemVmType.getVmTypeCpuNum();
            serverMemoryNumLeft = server.getServerMemoryNumLeftA() + server.getServerMemoryNumLeftB() - queueItemVmType.getVmTypeMemoryNum();
            ratioServerCpuNumLeft = (float) serverCpuNumLeft / (float) server.getServerType().getServerTypeCpuNum();
            ratioServerMemoryNumLeft = (float) serverMemoryNumLeft / (float) server.getServerType().getServerTypeMemoryNum();

            deployNode = constant.VM_NODE_AB;
        }

        return new MultipleReturn(ratioServerCpuNumLeft, ratioServerMemoryNumLeft, deployNode);
    }

    // 判断该服务器有无足够剩余空间
    private boolean hasEnoughSpace(VmType vmType, Server server) {

        if (vmType.getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE) {
            if ((server.getServerCpuNumLeftA() < vmType.getVmTypeCpuNum() || (server.getServerMemoryNumLeftA() < vmType.getVmTypeMemoryNum()) && server.getServerCpuNumLeftB() < vmType.getVmTypeCpuNum() || server.getServerMemoryNumLeftB() < vmType.getVmTypeMemoryNum())) {
                return false;
            }
        } else {
            if (server.getServerCpuNumLeftA() < vmType.getVmTypeCpuNum() / 2 || server.getServerCpuNumLeftB() < vmType.getVmTypeCpuNum() / 2 || server.getServerMemoryNumLeftA() < vmType.getVmTypeMemoryNum() / 2 || server.getServerMemoryNumLeftB() < vmType.getVmTypeMemoryNum()) {
                return false;
            }
        }

        return true;
    }

    // 处理删除请求
    private void processQueueItemDel(QueueItem queueItem) {
        int serverId = this.resourcePool.getVmServerMap().get(queueItem.getQueueItemVmId());

        // TODO: 可以优化，空间换时间维护 HashMap(serverId, Server)
        this.resourcePool.getServerList().forEach(
                server -> {
                    if (server.getServerId() == serverId) {
                        server.removeVm(queueItem.getQueueItemVmId());
                    }
                }
        );

        this.resourcePool.freeVm(queueItem.getQueueItemVmId());
    }


    // 处理周期的请求队列的前置操作
    private void beforeProcessPeriodQueue() {
        this.trainingData.getServerTypeList().forEach(
                serverType -> {
                    Server server = new Server(serverType);
                    this.resourcePool.buyServer(server);
                }
        );
    }

    // 处理当天的请求队列的前置操作
    private void beforeProcessDailyQueue() {
        if (constant.NEED_MIGRATION) {
            this.migrateVm();
        }
        this.dailyNewServerCount = 0;
        this.dailyVmIdOnNewServer.clear();
    }

    // 处理当天的请求队列的后置操作
    private void afterProcessDailyQueue(DailyQueue dailyQueue) {
        // 服务器类型 - 类型服务器数量
        HashMap<String, Integer> typeCountMap = new HashMap<>();

        // 分配服务器ID
        HashMap<Integer, Integer> oldNewServerIdMap = this.arrangeServerId(typeCountMap);
        this.updateVmServerId(oldNewServerIdMap);

        // 提交请使用此行
//        Output.output_daily(typeCountMap.size(), typeCountMap, this.dailyMigrationList.size(), this.dailyMigrationList, dailyQueue);
        // 测试请使用此行
        OutputFile.output_daily(typeCountMap.size(), typeCountMap, this.dailyMigrationList.size(), this.dailyMigrationList, dailyQueue);
        this.dailyMigrationList.clear();
    }

    // 分配服务器ID
    private HashMap<Integer, Integer> arrangeServerId(HashMap<String, Integer> typeCountMap) {
        // 服务器类型 - 类型服务器 id 起点
        HashMap<String, Integer> typeStartMap = new HashMap<>();
        // 服务器类型 - 类型服务器 offset 偏移
        HashMap<String, Integer> typeOffsetMap = new HashMap<>();

        // 新服务器类型集合
        ArrayList<String> typeList = new ArrayList<>();

        // 新旧服务器 id 映射
        HashMap<Integer, Integer> oldNewServerIdMap = new HashMap<>();


        // 第一次循环，统计类型和数量
        this.resourcePool.getServerList().forEach(
                server -> {
                    if (server.getServerId() <= constant.SERVER_ID_NEW_START) {
                        if (typeCountMap.containsKey(server.getServerType().getServerTypeName())) {
                            typeCountMap.put(server.getServerType().getServerTypeName(), typeCountMap.get(server.getServerType().getServerTypeName()) + 1);
                        } else {
                            typeCountMap.put(server.getServerType().getServerTypeName(), 1);
                        }

                        typeList.add(server.getServerType().getServerTypeName());
                    }
                }
        );

        int dailyServerCount = 0;
        for (String typeName : typeCountMap.keySet()) {
            typeStartMap.put(typeName, dailyServerCount + this.resourcePool.getRealServerCount());
            dailyServerCount += typeCountMap.get(typeName);
            typeOffsetMap.put(typeName, 0);
        }

        // 第二次循环，分配 server id
        this.resourcePool.getServerList().forEach(
                server -> {
                    if (server.getServerId() <= constant.SERVER_ID_NEW_START) {
                        // 计算得到新的 server id
                        int newServerId = typeStartMap.get(server.getServerType().getServerTypeName()) + typeOffsetMap.get(server.getServerType().getServerTypeName());
                        typeOffsetMap.put(server.getServerType().getServerTypeName(), typeOffsetMap.get(server.getServerType().getServerTypeName()) + 1);

                        // 记录当天临时 server id 与新的 server id 的关系
                        oldNewServerIdMap.put(server.getServerId(), newServerId);

                        // 赋予 server 以新的 id
                        server.setServerId(newServerId);
                    }
                }
        );

        // 更新真实服务器数量
        this.resourcePool.setRealServerCount(this.resourcePool.getRealServerCount() + dailyNewServerCount);
        return oldNewServerIdMap;
    }

    // 更新虚拟机对应的服务器 id
    private void updateVmServerId(HashMap<Integer, Integer> oldNewServerIdMap) {
        this.dailyVmIdOnNewServer.forEach(
                vmId -> {
                    int oldServerId = this.resourcePool.getVmServerMap().get(vmId);
                    this.resourcePool.getVmServerMap().put(vmId, oldNewServerIdMap.get(oldServerId));
                    this.resourcePool.getVmMap().get(vmId).setServerId(oldNewServerIdMap.get(oldServerId));
                }
        );
    }

    private void migrateVm() {
        int vmCount = this.resourcePool.getVmMap().size();
        int maxMigrationNum = 5 * vmCount / 1000;
        int migrationNum = 0;

        for (int vmId : this.resourcePool.getVmMap().keySet()) {
            // 超过最大迁移数量，直接退出
            if (migrationNum >= maxMigrationNum) {
                return;
            }

            Vm vm = this.resourcePool.getVmMap().get(vmId);
            int originServerId = vm.getServerId();
            Server originServer = new Server();

            float tempBestServerEvaluation = constant.MIN_VALUE_INITIAL;
            Server tempBestServer = new Server();
            String tempBestDeployNode = null;

            for (Server server : this.resourcePool.getServerList()) {
                // 找到原始 server
                if (server.getServerId() == originServerId) {
                    originServer = server;
                }
                // 不考虑虚拟服务器
                if (server.getServerId() < 0) {
                    continue;
                }

                // 判断该服务器剩余空间是否满足条件
                if (!this.hasEnoughSpace(vm.getVmType(), server)) {
                    continue;
                }

                // 指标 1, 2: CPU, Memory
                MultipleReturn ratioCpuAndMemoryLeft = this.calculateRatioCpuAndMemoryLeft(vm.getVmType(), server);
                float ratioServerCpuNumLeft = ratioCpuAndMemoryLeft.getFirst();
                float ratioServerMemoryNumLeft = ratioCpuAndMemoryLeft.getSecond();
                String deployNode = ratioCpuAndMemoryLeft.getThird();

                // 指标 3: CPU/Memory
                float ratioDensityGap = Math.abs(vm.getVmType().getVmTypeRatioDensity() - server.getServerType().getServerTypeRatioDensity());

                // 指标 4, 5: hardwareCost, runningCost
                float ratioHardwareCost = (float) server.getServerType().getServerTypeHardwareCost();
                float ratioRunningCost = (float) server.getServerType().getServerTypeRunningCost();

                // 评价结果
                float serverEvaluation = this.calculateServerEvaluationForMigration(ratioServerCpuNumLeft, ratioServerMemoryNumLeft, ratioDensityGap, ratioHardwareCost, ratioRunningCost);

                if (serverEvaluation < tempBestServerEvaluation) {
                    tempBestServerEvaluation = serverEvaluation;
                    tempBestServer = server;
                    tempBestDeployNode = deployNode;
                }
            }

            if (originServerId != tempBestServer.getServerId() && tempBestServer.getServerId() > 0) {
                originServer.removeVm(vmId);
                vm.setServerId(tempBestServer.getServerId());
                vm.setDeployNode(tempBestDeployNode);
                tempBestServer.deployVm(vm, tempBestDeployNode);
                this.resourcePool.getVmServerMap().put(vmId, tempBestServer.getServerId());
                migrationNum++;
                this.dailyMigrationList.add(new MigrationItem(vmId, tempBestServer.getServerId(), tempBestDeployNode));
            }
        }
    }
}
