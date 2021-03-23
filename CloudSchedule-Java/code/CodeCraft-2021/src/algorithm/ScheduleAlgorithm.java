package algorithm;

import pojo.*;


public class ScheduleAlgorithm {
    private TrainingData trainingData;
    private ResourcePool resourcePool;

    private int dailyNewServerCount;

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
        if(queueItem.getQueueItemAction().equals("")){

        }
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
