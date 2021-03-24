package pojo;


public class QueueItem {
    private String queueItemAction;
    private VmType queueItemVmType;
    private int queueItemVmId;

    private Vm queueVm;

    public QueueItem(String queueItemAction, VmType queueItemVmType, int queueItemVmId) {
        this.queueItemAction = queueItemAction;
        this.queueItemVmType = queueItemVmType;
        this.queueItemVmId = queueItemVmId;
        this.queueVm = new Vm(queueItemVmType, queueItemVmId);
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

    public VmType getQueueItemVmType() {
        return queueItemVmType;
    }

    public void setQueueItemVmType(VmType queueItemVmtype) {
        this.queueItemVmType = queueItemVmtype;
    }

    public int getQueueItemVmId() {
        return queueItemVmId;
    }

    public void setQueueItemVmId(int queueItemVmId) {
        this.queueItemVmId = queueItemVmId;
    }

    public Vm getQueueVm() {
        return queueVm;
    }

    public void setQueueVm(Vm queueVm) {
        this.queueVm = queueVm;
    }
}
