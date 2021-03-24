package algorithm;

import pojo.Server;
import pojo.ServerType;
import pojo.Vm;
import pojo.VmType;

import java.util.ArrayList;
import java.util.HashMap;


public class ResourcePool {
    // 服务器列表
    private ArrayList<Server> serverList = new ArrayList<>();
    // 虚拟机 map
    private HashMap<Integer, Vm> vmMap = new HashMap<>();

    private HashMap<Integer, Integer> vmServerMap = new HashMap<>();

    private int realServerCount;

    public ResourcePool() {

    }

    public Vm createVm(int vmId, VmType vmType){
        Vm createdVm = new Vm(vmType, vmId);
        this.vmMap.put(vmId, createdVm);
        return createdVm;
    }

    public void freeVm(int vmId){
        this.vmMap.remove(vmId);
    }

    public void buyServer(Server server){
        // 增加虚拟服务器
        this.serverList.add(new Server(server.getServerType()));
    }

    public void display() {
        System.out.println(String.format("ResourcePool: %d servers", this.serverList.size()));
        this.getServerList().forEach(
                server -> {
                    System.out.println(String.format("StringId: %d, VmNum: %d", server.getServerId(), server.getVmMap().size()));
                }
        );
    }

    public ArrayList<Server> getServerList() {
        return serverList;
    }

    public void setServerList(ArrayList<Server> serverList) {
        this.serverList = serverList;
    }

    public HashMap<Integer, Vm> getVmMap() {
        return vmMap;
    }

    public void setVmMap(HashMap<Integer, Vm> vmMap) {
        this.vmMap = vmMap;
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
