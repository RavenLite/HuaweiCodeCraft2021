package com.huawei.java.main;

import algorithm.ResourcePool;
import algorithm.ScheduleAlgorithm;
import pojo.*;
import utils.Read;
import utils.ReadFile;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        // TODO: Read standard input
        // TODO: process
        // TODO: write standard Output
        // TODO: System.out.flush()

        // 提交时请使用此行，同时请调整 ScheduleAlgorithm.java 的输出部分
//        new ScheduleAlgorithm(new Read().read(), new ResourcePool()).processPeriodQueue();

        // 测试时请使用此行，同时请调整 ScheduleAlgorithm.java 的输出部分
        new ScheduleAlgorithm(new ReadFile().get_training_data(), new ResourcePool()).processPeriodQueue();
        System.out.flush();
    }
}