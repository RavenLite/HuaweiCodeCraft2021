package algorithm;

import pojo.*;
import utils.Constant;
import utils.MultipleReturn;

import java.util.ArrayList;
import java.util.HashMap;


public class ScheduleAlgorithm {
    private TrainingData trainingData;
    private ResourcePool resourcePool;

    private int dailyNewServerCount;
    private static Constant constant = new Constant();

    // 记录了当天购买了新服务器的虚拟机 ID
    private ArrayList<Integer> dailyVmIdOnNewServer = new ArrayList<>();

    public ScheduleAlgorithm(TrainingData trainingData, ResourcePool resourcePool) {
        this.trainingData = trainingData;
        this.resourcePool = resourcePool;

        this.dailyNewServerCount = 0;
    }

    // 处理周期的请求队列
    public void processPeriodQueue(){
        this.beforeProcessPeriodQueue();

        this.trainingData.getDailyQueueList().forEach(
                dailyQueue -> {
                    // 命令行提示
                    String str = String.format("Running: %d/%d, ServerCount: %d", this.trainingData.getDailyQueueList().indexOf(dailyQueue) + 1, this.trainingData.getDailyQueueNum(), this.resourcePool.getServerList().size());
                    System.out.println(str);

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

        this.afterProcessDailyQueue();
    }

    // 处理当天的每一条请求
    private void processQueueItem(QueueItem queueItem){
        if(constant.ACTION_ADD.equals(queueItem.getQueueItemAction())){
            this.processQueueItemAdd(queueItem);
        } else {
            this.processQueueItemDel(queueItem);
        }
    }

    // 处理添加请求
    private void processQueueItemAdd(QueueItem queueItem){
        VmType queueItemVmType = queueItem.getQueueItemVmType();

        // 临时最优变量
        var ref = new Object() {
            float bestServerEvaluation = constant.MIN_VALUE_INITIAL;
            Server bestServer;
            String bestDeployNode;
        };

        this.resourcePool.getServerList().forEach(
                server -> {
                    // 判断该服务器剩余空间是否满足条件
                    if(!this.hasEnoughSpace(queueItem, server)){
                        return;
                    }

                    // 指标 1, 2: CPU, Memory
                    MultipleReturn ratioCpuAndMemoryLeft = this.calculateRatioCpuAndMemoryLeft(queueItemVmType, server);
                    float ratioServerCpuNumLeft = ratioCpuAndMemoryLeft.getFirst();
                    float ratioServerMemoryNumLeft = ratioCpuAndMemoryLeft.getSecond();
                    String deployNode = ratioCpuAndMemoryLeft.getThird();

                    // 指标 3: CPU/Memory
                    float ratioDensityGap = Math.abs(queueItemVmType.getVmTypeRatioDensity() - server.getServerType().getServerTypeRatioDensity());

                    // 指标 4, 5: hardwareCost, runningCost
                    float ratioHardwareCost = (float)server.getServerType().getServerTypeHardwareCost();
                    float ratioRunningCost = (float)server.getServerType().getServerTypeRunningCost();

                    // 评价结果
                    float serverEvaluation = this.calculateServerEvaluation(ratioServerCpuNumLeft, ratioServerMemoryNumLeft, ratioDensityGap, ratioHardwareCost, ratioRunningCost);

                    // 处理更优情况
                    if (serverEvaluation < ref.bestServerEvaluation){
                        ref.bestServerEvaluation = serverEvaluation;
                        ref.bestServer = server;
                        ref.bestDeployNode = deployNode;
                    }
                }
        );

        // 处理最优情况
        this.handleBetterResult(queueItem, ref.bestServer, ref.bestDeployNode);
    }

    // 处理最优情况
    private void handleBetterResult(QueueItem queueItem, Server server, String deployNode) {
        server.deployVm(queueItem.getQueueVm(), deployNode);

        // 判断是否需要新购买服务器
        if(server.getServerId() == constant.SERVER_ID_VIRTUAL) {
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
            queueItem.getQueueVm().setServerId(server.getServerId());
            queueItem.getQueueVm().setDeployNode(deployNode);
        }

        this.resourcePool.getVmServerMap().put(queueItem.getQueueItemVmId(), server.getServerId());
    }

    // 评价算法
    // TODO: 复杂化
    private float calculateServerEvaluation(float ratioServerCpuNumLeft, float ratioServerMemoryNumLeft, float ratioDensityGap, float ratioHardwareCost, float ratioRunningCost){
        float serverEvaluation = ratioServerCpuNumLeft * 10 + ratioServerMemoryNumLeft * 10 + ratioDensityGap * 10 + ratioHardwareCost / 20000 + ratioRunningCost / 50;
        return serverEvaluation;
    }

    private MultipleReturn calculateRatioCpuAndMemoryLeft(VmType queueItemVmType, Server server){
        int serverCpuNumLeft;
        int serverMemoryNumLeft;
        float ratioServerCpuNumLeft;
        float ratioServerMemoryNumLeft;
        String deployNode = null;

        if (queueItemVmType.getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE){
            if(server.getServerCpuNumLeftA() < queueItemVmType.getVmTypeCpuNum() && server.getServerMemoryNumLeftA() < queueItemVmType.getVmTypeMemoryNum()) {
                serverCpuNumLeft = server.getServerCpuNumLeftA() - queueItemVmType.getVmTypeCpuNum();
                serverMemoryNumLeft = server.getServerMemoryNumLeftA() - queueItemVmType.getVmTypeMemoryNum();
                ratioServerCpuNumLeft = (float)serverCpuNumLeft / (float)(server.getServerType().getServerTypeCpuNum() / 2);
                ratioServerMemoryNumLeft = (float)serverMemoryNumLeft / (float)(server.getServerType().getServerTypeMemoryNum() / 2);

                deployNode = constant.VM_NODE_A;
            } else {
                serverCpuNumLeft = server.getServerCpuNumLeftB() - queueItemVmType.getVmTypeCpuNum();
                serverMemoryNumLeft = server.getServerMemoryNumLeftB() - queueItemVmType.getVmTypeMemoryNum();
                ratioServerCpuNumLeft = (float)serverCpuNumLeft / (float)(server.getServerType().getServerTypeCpuNum() / 2);
                ratioServerMemoryNumLeft = (float)serverMemoryNumLeft / (float)(server.getServerType().getServerTypeMemoryNum() / 2);

                deployNode = constant.VM_NODE_B;
            }
        } else {
            serverCpuNumLeft = server.getServerCpuNumLeftA() + server.getServerCpuNumLeftA() - queueItemVmType.getVmTypeCpuNum();
            serverMemoryNumLeft = server.getServerMemoryNumLeftA() + server.getServerMemoryNumLeftB() - queueItemVmType.getVmTypeMemoryNum();
            ratioServerCpuNumLeft = (float)serverCpuNumLeft / (float)server.getServerType().getServerTypeCpuNum();
            ratioServerMemoryNumLeft = (float)serverMemoryNumLeft / (float)server.getServerType().getServerTypeMemoryNum();
        }

        return new MultipleReturn(ratioServerCpuNumLeft, ratioServerMemoryNumLeft, deployNode);
    }

    // 判断该服务器有无足够剩余空间
    private boolean hasEnoughSpace(QueueItem queueItem, Server server){
        if(queueItem.getQueueItemVmType().getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE){
            if((server.getServerCpuNumLeftA() < queueItem.getQueueItemVmType().getVmTypeCpuNum() && server.getServerCpuNumLeftB() < queueItem.getQueueItemVmType().getVmTypeCpuNum()) || (server.getServerMemoryNumLeftA() < queueItem.getQueueItemVmType().getVmTypeMemoryNum() && server.getServerMemoryNumLeftB() < queueItem.getQueueItemVmType().getVmTypeMemoryNum())){
                return false;
            }
        } else {
            if (server.getServerCpuNumLeftA() < queueItem.getQueueItemVmType().getVmTypeCpuNum() / 2 || server.getServerCpuNumLeftB() < queueItem.getQueueItemVmType().getVmTypeCpuNum() / 2 || server.getServerMemoryNumLeftA() < queueItem.getQueueItemVmType().getVmTypeMemoryNum() / 2 || server.getServerMemoryNumLeftB() < queueItem.getQueueItemVmType().getVmTypeMemoryNum()){
                return false;
            }
        }

        return true;
    }

    // 处理删除请求
    private void processQueueItemDel(QueueItem queueItem){
        int serverId = this.resourcePool.getVmServerMap().get(queueItem.getQueueItemVmId());

        // TODO: 可以优化，空间换时间维护 HashMap(serverId, Server)
        this.resourcePool.getServerList().forEach(
                server -> {
                    if(server.getServerId() == serverId){
                        server.removeVm(queueItem.getQueueItemVmId());
                    }
                }
        );
    }


    // 处理周期的请求队列的前置操作
    private void beforeProcessPeriodQueue(){
        this.trainingData.getServerTypeList().forEach(
                serverType -> {
                    Server server = new Server(serverType);
                    this.resourcePool.buyServer(server);
                }
        );
    }

    // 处理当天的请求队列的前置操作
    private void beforeProcessDailyQueue(){
        this.migrateVm();
        this.dailyNewServerCount = 0;
        this.dailyVmIdOnNewServer.clear();
    }

    // 处理当天的请求队列的后置操作
    private void afterProcessDailyQueue(){
        // 分配服务器ID
        HashMap<Integer, Integer> oldNewServerIdMap = this.arrangeServerId();
        this.updateVmServerId(oldNewServerIdMap);
    }

    // 分配服务器ID
    private HashMap<Integer, Integer> arrangeServerId() {
        // 服务器类型 - 类型服务器数量
        HashMap<String, Integer> typeCountMap = new HashMap<>();
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
                    if (server.getServerId() <= constant.SERVER_ID_NEW_START){
                        if (typeCountMap.containsKey(server.getServerType().getServerTypeName())){
                            typeCountMap.put(server.getServerType().getServerTypeName(), typeCountMap.get(server.getServerType().getServerTypeName()) + 1);
                        } else {
                            typeCountMap.put(server.getServerType().getServerTypeName(), 1);
                        }

                        typeList.add(server.getServerType().getServerTypeName());
                    }
                }
        );

        int dailyServerCount = 0;
        for(String typeName : typeCountMap.keySet()) {
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

        return oldNewServerIdMap;
    }

    // 更新虚拟机对应的服务器 id
    private void updateVmServerId(HashMap<Integer, Integer> oldNewServerIdMap) {
        this.dailyVmIdOnNewServer.forEach(
                vmId -> {
                    this.resourcePool.getVmServerMap().put(vmId, oldNewServerIdMap.get(this.resourcePool.getVmServerMap().get(vmId)));
                }
        );
    }

    private void migrateVm(){

    }
}
