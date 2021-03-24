package pojo;


import utils.Constant;

import java.util.HashMap;


public class Server {
    private int serverId;
    private ServerType serverType;
    private int serverCpuNumLeftA;
    private int serverCpuNumLeftB;
    private int serverMemoryNumLeftA;
    private int serverMemoryNumLeftB;

    private HashMap<Integer, Vm> vmMap;

    private static Constant constant;

    public Server(ServerType serverType){
        this.serverId = -1;
        this.serverType = serverType;
        this.serverCpuNumLeftA = serverType.getServerTypeCpuNum() / 2;
        this.serverCpuNumLeftB = serverType.getServerTypeCpuNum() / 2;
        this.serverMemoryNumLeftA = serverType.getServerTypeMemoryNum() / 2;
        this.serverMemoryNumLeftB = serverType.getServerTypeMemoryNum() / 2;
    }

    public void deployVm(Vm vm, String deployNode){
        if (vm.getVmType().getVmTypeDeploymentWay() == constant.VM_DEPLOYMENT_SINGLE){
            if(constant.VM_NODE_A.equals(deployNode)){
                this.serverCpuNumLeftA -= vm.getVmType().getVmTypeCpuNum();
                this.serverMemoryNumLeftA -= vm.getVmType().getVmTypeMemoryNum();
            } else {
                this.serverCpuNumLeftB -= vm.getVmType().getVmTypeCpuNum();
                this.serverMemoryNumLeftB -= vm.getVmType().getVmTypeMemoryNum();
            }
        } else {
            this.serverCpuNumLeftA -= vm.getVmType().getVmTypeCpuNum() / 2;
            this.serverCpuNumLeftB -= vm.getVmType().getVmTypeCpuNum() / 2;
            this.serverMemoryNumLeftA -= vm.getVmType().getVmTypeMemoryNum() / 2;
            this.serverMemoryNumLeftB -= vm.getVmType().getVmTypeMemoryNum() / 2;
        }

        this.vmMap.put(vm.getVmId(), vm);
    }

    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public int getServerId() {
        return serverId;
    }

    public void setServerId(int serverId) {
        this.serverId = serverId;
    }

    public ServerType getServerType() {
        return serverType;
    }

    public void setServerType(ServerType serverType) {
        this.serverType = serverType;
    }

    public int getServerCpuNumLeftA() {
        return serverCpuNumLeftA;
    }

    public void setServerCpuNumLeftA(int serverCpuNumLeftA) {
        this.serverCpuNumLeftA = serverCpuNumLeftA;
    }

    public int getServerCpuNumLeftB() {
        return serverCpuNumLeftB;
    }

    public void setServerCpuNumLeftB(int serverCpuNumLeftB) {
        this.serverCpuNumLeftB = serverCpuNumLeftB;
    }

    public int getServerMemoryNumLeftA() {
        return serverMemoryNumLeftA;
    }

    public void setServerMemoryNumLeftA(int serverMemoryNumLeftA) {
        this.serverMemoryNumLeftA = serverMemoryNumLeftA;
    }

    public int getServerMemoryNumLeftB() {
        return serverMemoryNumLeftB;
    }

    public void setServerMemoryNumLeftB(int serverMemoryNumLeftB) {
        this.serverMemoryNumLeftB = serverMemoryNumLeftB;
    }
}
