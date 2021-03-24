package pojo;


public class ServerType {
    private String serverTypeName;
    private int serverTypeCpuNum;
    private int serverTypeMemoryNum;
    private int serverTypeHardwareCost;
    private int serverTypeRunningCost;
    private float serverTypeRatioDensity;

    public ServerType(String serverTypeName, int serverTypeCpuNum, int serverTypeMemoryNum, int serverTypeHardwareCost, int serverTypeRunningCost){
        this.serverTypeName = serverTypeName;
        this.serverTypeCpuNum = serverTypeCpuNum;
        this.serverTypeMemoryNum = serverTypeMemoryNum;
        this.serverTypeHardwareCost = serverTypeHardwareCost;
        this.serverTypeRunningCost = serverTypeRunningCost;

        this.serverTypeRatioDensity = (float)serverTypeCpuNum / (float)serverTypeMemoryNum;
    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public String getServerTypeName() {
        return serverTypeName;
    }

    public void setServerTypeName(String serverTypeName) {
        this.serverTypeName = serverTypeName;
    }

    public int getServerTypeCpuNum() {
        return serverTypeCpuNum;
    }

    public void setServerTypeCpuNum(int serverTypeCpuNum) {
        this.serverTypeCpuNum = serverTypeCpuNum;
    }

    public int getServerTypeMemoryNum() {
        return serverTypeMemoryNum;
    }

    public void setServerTypeMemoryNum(int serverTypeMemoryNum) {
        this.serverTypeMemoryNum = serverTypeMemoryNum;
    }

    public int getServerTypeHardwareCost() {
        return serverTypeHardwareCost;
    }

    public void setServerTypeHardwareCost(int serverTypeHardwareCost) {
        this.serverTypeHardwareCost = serverTypeHardwareCost;
    }

    public int getServerTypeRunningCost() {
        return serverTypeRunningCost;
    }

    public void setServerTypeRunningCost(int serverTypeRunningCost) {
        this.serverTypeRunningCost = serverTypeRunningCost;
    }

    public float getServerTypeRatioDensity() {
        return serverTypeRatioDensity;
    }

    public void setServerTypeRatioDensity(float serverTypeRatioDensity) {
        this.serverTypeRatioDensity = serverTypeRatioDensity;
    }
}
