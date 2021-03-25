package pojo;


public class Vm {
    private VmType vmType;
    private int vmId;

    private int serverId;
    private String deployNode;

    public Vm(VmType vmType, int vmId) {
        this.vmType = vmType;
        this.vmId = vmId;
    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public VmType getVmType() {
        return vmType;
    }

    public void setVmType(VmType vmType) {
        this.vmType = vmType;
    }

    public int getVmId() {
        return vmId;
    }

    public void setVmId(int vmId) {
        this.vmId = vmId;
    }

    public int getServerId() {
        return serverId;
    }

    public void setServerId(int serverId) {
        this.serverId = serverId;
    }

    public String getDeployNode() {
        return deployNode;
    }

    public void setDeployNode(String deployNode) {
        this.deployNode = deployNode;
    }
}
