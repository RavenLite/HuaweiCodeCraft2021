package algorithm;

import pojo.*;
import utils.Constant;
import utils.MultipleReturn;


public class ScheduleAlgorithm {
    private TrainingData trainingData;
    private ResourcePool resourcePool;

    private int dailyNewServerCount;
    private static Constant constant;

    public ScheduleAlgorithm(TrainingData trainingData, ResourcePool resourcePool) {
        this.trainingData = trainingData;
        this.resourcePool = resourcePool;

        this.dailyNewServerCount = 0;
    }

    public void processPeriodQueue(){
        this.trainingData.getDailyQueueList().forEach(
                dailyQueue -> {
                    // 命令行提示
                    String str = String.format("Running: %d/%d, ServerCount: %d", this.trainingData.getDailyQueueList().indexOf(dailyQueue), this.trainingData.getDailyQueueNum(), this.resourcePool.getServerList().size());
                    System.out.println(str);

                    this.processDailyQueue(dailyQueue);
                }
        );
    }

    private void processDailyQueue(DailyQueue dailyQueue) {
        this.beforeProcessDailyQueue();

        dailyQueue.getQueueItemList().forEach(
                this::processQueueItem
        );
    }

    private void processQueueItem(QueueItem queueItem){
        if(constant.ACTION_ADD.equals(queueItem.getQueueItemAction())){
            this.processQueueItemAdd(queueItem);
        } else {
            this.processQueueItem(queueItem);
        }
    }

    private void processQueueItemAdd(QueueItem queueItem){
        VmType queueItemVmType = queueItem.getQueueItemVmType();

        // 临时最优变量
        var ref = new Object() {
            float bestServerEvaluation = constant.MIN_VALUE_INITIAL;
            Server bestServer;
        };

        // 记录 cpu，memory 剩余的临时变量
        int currentCpuNumLeftA = constant.NUM_ZERO;
        int currentCpuNumLeftB = constant.NUM_ZERO;
        int currentMemoryNumLeftA = constant.NUM_ZERO;
        int currentMemoryNumLeftB = constant.NUM_ZERO;
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
                        this.handleBetterResult(queueItem, server, deployNode);
                        ref.bestServerEvaluation = serverEvaluation;
                        ref.bestServer = server;
                    }
                }
        );

    }

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
        } else {
            queueItem.getQueueVm().setServerId(server.getServerId());
            queueItem.getQueueVm().setDeployNode(deployNode);
        }

    }

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

    private void processQueueItemDel(QueueItem queueItem){

    }


    // 处理每一天的请求队列的前置操作
    private void beforeProcessPeriodQueue(){
        this.trainingData.getServerTypeList().forEach(
                serverType -> {
                    Server server = new Server(serverType);
                    this.resourcePool.buyServer(server);
                }
        );
    }

    private void beforeProcessDailyQueue(){
        this.migrateVm();
        this.dailyNewServerCount = 0;
    }

    private void migrateVm(){

    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public TrainingData getTrainingData() {
        return trainingData;
    }

    public void setTrainingData(TrainingData trainingData) {
        this.trainingData = trainingData;
    }

    public ResourcePool getResourcePool() {
        return resourcePool;
    }

    public void setResourcePool(ResourcePool resourcePool) {
        this.resourcePool = resourcePool;
    }
}
