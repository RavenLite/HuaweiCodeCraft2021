package algorithm;

import pojo.Server;
import pojo.ServerType;
import pojo.Vm;

import java.util.ArrayList;


public class ResourcePool {
    private ArrayList<Server> serverList;
    private ArrayList<Vm> vmList;

    public void buyServer(Server server){
        this.serverList.add(server);
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
}
