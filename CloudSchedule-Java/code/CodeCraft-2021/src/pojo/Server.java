package pojo;

/**
 * @Author: Raven
 * @Date: 2021/3/23 8:52 PM
 */
public class Server {
    private int serverId;
    private ServerType serverType;
    private int serverCpuNumLeftA;
    private int serverCpuNumLeftB;
    private int serverMemoryNumLeftA;
    private int serverMemoryNumLeftB;

    public Server(ServerType serverType, int serverCpuNumLeftA, int serverCpuNumLeftB, int serverMemoryNumLeftA, int serverMemoryNumLeftB){
        this.serverId = -1;
        this.serverType = serverType;
        this.serverCpuNumLeftA = serverCpuNumLeftA;
        this.serverCpuNumLeftB = serverCpuNumLeftB;
        this.serverMemoryNumLeftA = serverMemoryNumLeftA;
        this.serverMemoryNumLeftB = serverMemoryNumLeftB;
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
