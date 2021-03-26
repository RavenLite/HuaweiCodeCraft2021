package utils;

/**
 * @Author: Raven
 * @Date: 2021/3/23 10:50 PM
 */
public class Constant {
    // queue item action
    public String ACTION_ADD = "add";
    public String ACTION_DEL = "del";
    // vm deployment way
    public int VM_DEPLOYMENT_SINGLE = 0;
    public int VM_DEPLOYMENT_DOUBLE = 1;
    // vm node name
    public String VM_NODE_A = "A";
    public String VM_NODE_B = "B";
    public String VM_NODE_AB = "AB";

    // constant
    public int NUM_ZERO = 0;
    public String STRING_EMPTY = "";
    public float MIN_VALUE_INITIAL = 1000000;

    // server id
    public int SERVER_ID_VIRTUAL = -1;
    public int SERVER_ID_NEW_START = -2;

    // weight for add
//    public float WEIGHT_SERVER_CPU_NUM_LEFT = 1.0f;
//    public float WEIGHT_SERVER_MEMORY_NUM_LEFT = 1.0f;
//    public float WEIGHT_DENSITY_GAP = 1.0f;
//    public float WEIGHT_HARDWARE_COST = 1.0f;
//    public float WEIGHT_RUNNING_COST = 1.0f;

    public float WEIGHT_SERVER_SPACE_LEFT = 1.0f;
    public float WEIGHT_SERVER_DENSITY_GAP = 1.0f;
    public float WEIGHT_SERVER_COST = 1.0f;

    // weight for migration
//    public float WEIGHT_SERVER_CPU_NUM_LEFT_MIGRATION = 1.0f;
//    public float WEIGHT_SERVER_MEMORY_NUM_LEFT_MIGRATION = 1.0f;
//    public float WEIGHT_DENSITY_GAP_MIGRATION = 1.0f;
//    public float WEIGHT_HARDWARE_COST_MIGRATION = 1.0f;
//    public float WEIGHT_RUNNING_COST_MIGRATION = 1.0f;

    public float WEIGHT_SERVER_SPACE_LEFT_MIGRATION = 1.0f;
    public float WEIGHT_SERVER_DENSITY_GAP_MIGRATION = 1.0f;
    public float WEIGHT_SERVER_COST_MIGRATION = 1.0f;

    // switch
    public boolean NEED_MIGRATION = true;
}
