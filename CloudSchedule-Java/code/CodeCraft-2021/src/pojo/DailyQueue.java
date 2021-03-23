package pojo;

import java.util.ArrayList;


public class DailyQueue {
    private int queueItemNum;
    private ArrayList<QueueItem> queueItemList;

    public DailyQueue(int queueItemNum, ArrayList<QueueItem> queueItemList) {
        this.queueItemNum = queueItemNum;
        this.queueItemList = queueItemList;
    }

    public int getQueueItemNum() {
        return queueItemNum;
    }

    public void setQueueItemNum(int queueItemNum) {
        this.queueItemNum = queueItemNum;
    }

    public ArrayList<QueueItem> getQueueItemList() {
        return queueItemList;
    }

    public void setQueueItemList(ArrayList<QueueItem> queueItemList) {
        this.queueItemList = queueItemList;
    }
}
