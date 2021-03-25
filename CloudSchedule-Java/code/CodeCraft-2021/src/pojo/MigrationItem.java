package pojo;

/**
 * @Author: Raven
 * @Date: 2021/3/25 5:46 PM
 */
public class MigrationItem {
    private int vmId;
    private int serverId;
    private String deploymentNode;

    public MigrationItem(int vmId, int serverId, String deploymentNode) {
        this.vmId = vmId;
        this.serverId = serverId;
        this.deploymentNode = deploymentNode;
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

    public String getDeploymentNode() {
        return deploymentNode;
    }

    public void setDeploymentNode(String deploymentNode) {
        this.deploymentNode = deploymentNode;
    }
}
