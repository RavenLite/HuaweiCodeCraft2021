package pojo;


public class QueueItem {
    private String queueItemAction;
    private VmType queueItemVmType;
    private int queueItemVmId;

    public QueueItem(String queueItemAction, VmType queueItemVmType, int queueItemVmId) {
        this.queueItemAction = queueItemAction;
        this.queueItemVmType = queueItemVmType;
        this.queueItemVmId = queueItemVmId;
    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public String getQueueItemAction() {
        return queueItemAction;
    }

    public void setQueueItemAction(String queueItemAction) {
        this.queueItemAction = queueItemAction;
    }

    public VmType getQueueItemVmtype() {
        return queueItemVmType;
    }

    public void setQueueItemVmtype(VmType queueItemVmtype) {
        this.queueItemVmType = queueItemVmtype;
    }

    public int getQueueItemVmId() {
        return queueItemVmId;
    }

    public void setQueueItemVmId(int queueItemVmId) {
        this.queueItemVmId = queueItemVmId;
    }
}
