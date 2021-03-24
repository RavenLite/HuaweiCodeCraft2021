package pojo;


public class VmType {
    private String vmTypeName;
    private int vmTypeCpuNum;
    private int vmTypeMemoryNum;
    private int vmTypeDeploymentWay;
    private float vmTypeRatioDensity;

    public VmType(String vmTypeName, int vmTypeCpuNum, int vmTypeMemoryNum, int vmTypeDeploymentWay){
        this.vmTypeName = vmTypeName;
        this.vmTypeCpuNum = vmTypeCpuNum;
        this.vmTypeMemoryNum = vmTypeMemoryNum;
        this.vmTypeDeploymentWay = vmTypeDeploymentWay;

        this.vmTypeRatioDensity = (float)vmTypeCpuNum / (float)vmTypeMemoryNum;
    }


    /**
     * 下面是 getter 和 setter 方法，无需关注
     */
    public String getVmTypeName() {
        return vmTypeName;
    }

    public void setVmTypeName(String vmTypeName) {
        this.vmTypeName = vmTypeName;
    }

    public int getVmTypeCpuNum() {
        return vmTypeCpuNum;
    }

    public void setVmTypeCpuNum(int vmTypeCpuNum) {
        this.vmTypeCpuNum = vmTypeCpuNum;
    }

    public int getVmTypeMemoryNum() {
        return vmTypeMemoryNum;
    }

    public void setVmTypeMemoryNum(int vmTypeMemoryNum) {
        this.vmTypeMemoryNum = vmTypeMemoryNum;
    }

    public int getVmTypeDeploymentWay() {
        return vmTypeDeploymentWay;
    }

    public void setVmTypeDeploymentWay(int vmTypeDeploymentWay) {
        this.vmTypeDeploymentWay = vmTypeDeploymentWay;
    }

    public float getVmTypeRatioDensity() {
        return vmTypeRatioDensity;
    }

    public void setVmTypeRatioDensity(float vmTypeRatioDensity) {
        this.vmTypeRatioDensity = vmTypeRatioDensity;
    }
}
