package utils;

/**
 * @Author: Raven
 * @Date: 2021/3/24 3:14 PM
 */
public class MultipleReturn {
    private final float first;
    private final float second;
    private final String deployNode;

    public MultipleReturn(float first, float second, String deployNode) {
        this.first = first;
        this.second = second;
        this.deployNode = deployNode;
    }

    public float getFirst() {
        return first;
    }

    public float getSecond() {
        return second;
    }

    public String getThird() {
        return deployNode;
    }
}
