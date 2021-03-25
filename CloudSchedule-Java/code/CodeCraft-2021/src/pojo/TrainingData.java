package pojo;

import java.util.ArrayList;
import java.util.HashMap;


public class TrainingData {
    private int serverTypeNum;
    private HashMap<String, ServerType> serverTypeMap;
    private ArrayList<ServerType> serverTypeList;

    private int vmTypeNum;
    private HashMap<String, VmType> vmTypeMap;
    private ArrayList<VmType> vmTypeList;

    private int dailyQueueNum;
    private ArrayList<DailyQueue> dailyQueueList;

    public TrainingData(int serverTypeNum, HashMap<String, ServerType> serverTypeMap, ArrayList<ServerType> serverTypeList, int vmTypeNum, HashMap<String, VmType> vmTypeMap, ArrayList<VmType> vmTypeList, int dailyQueueNum, ArrayList<DailyQueue> dailyQueueList) {
        this.serverTypeNum = serverTypeNum;
        this.serverTypeMap = serverTypeMap;
        this.serverTypeList = serverTypeList;
        this.vmTypeNum = vmTypeNum;
        this.vmTypeMap = vmTypeMap;
        this.vmTypeList = vmTypeList;
        this.dailyQueueNum = dailyQueueNum;
        this.dailyQueueList = dailyQueueList;
    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public int getServerTypeNum() {
        return serverTypeNum;
    }

    public void setServerTypeNum(int serverTypeNum) {
        this.serverTypeNum = serverTypeNum;
    }

    public HashMap<String, ServerType> getServerTypeMap() {
        return serverTypeMap;
    }

    public void setServerTypeMap(HashMap<String, ServerType> serverTypeMap) {
        this.serverTypeMap = serverTypeMap;
    }

    public ArrayList<ServerType> getServerTypeList() {
        return serverTypeList;
    }

    public void setServerTypeList(ArrayList<ServerType> serverTypeList) {
        this.serverTypeList = serverTypeList;
    }

    public int getVmTypeNum() {
        return vmTypeNum;
    }

    public void setVmTypeNum(int vmTypeNum) {
        this.vmTypeNum = vmTypeNum;
    }

    public HashMap<String, VmType> getVmTypeMap() {
        return vmTypeMap;
    }

    public void setVmTypeMap(HashMap<String, VmType> vmTypeMap) {
        this.vmTypeMap = vmTypeMap;
    }

    public ArrayList<VmType> getVmTypeList() {
        return vmTypeList;
    }

    public void setVmTypeList(ArrayList<VmType> vmTypeList) {
        this.vmTypeList = vmTypeList;
    }

    public int getDailyQueueNum() {
        return dailyQueueNum;
    }

    public void setDailyQueueNum(int dailyQueueNum) {
        this.dailyQueueNum = dailyQueueNum;
    }

    public ArrayList<DailyQueue> getDailyQueueList() {
        return dailyQueueList;
    }

    public void setDailyQueueList(ArrayList<DailyQueue> dailyQueueList) {
        this.dailyQueueList = dailyQueueList;
    }
}