package algorithm;

import pojo.Server;
import pojo.ServerType;
import pojo.Vm;

import java.util.ArrayList;
import java.util.HashMap;


public class ResourcePool {
    private ArrayList<Server> serverList;
    private ArrayList<Vm> vmList;

    private HashMap<Integer, Integer> vmServerMap;

    private int realServerCount;

    public ResourcePool() {

    }

    public void buyServer(Server server){
        // 增加虚拟服务器
        this.serverList.add(new Server(server.getServerType()));
    }

    public ArrayList<Server> getServerList() {
        return serverList;
    }

    public void setServerList(ArrayList<Server> serverList) {
        this.serverList = serverList;
    }

    public ArrayList<Vm> getVmList() {
        return vmList;
    }

    public void setVmList(ArrayList<Vm> vmList) {
        this.vmList = vmList;
    }

    public HashMap<Integer, Integer> getVmServerMap() {
        return vmServerMap;
    }

    public void setVmServerMap(HashMap<Integer, Integer> vmServerMap) {
        this.vmServerMap = vmServerMap;
    }

    public int getRealServerCount() {
        return realServerCount;
    }

    public void setRealServerCount(int realServerCount) {
        this.realServerCount = realServerCount;
    }
}
