package com.huawei.java.main;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        // TODO: read standard input
        // TODO: process
        // TODO: write standard output
        // TODO: System.out.flush()
        try {
            BufferedReader in = new BufferedReader(new FileReader("./CloudSchedule/training_data/training-1.txt"));

            int server_type_num = Integer.parseInt(in.readLine());


            String str;
            int i = 0;
            while ((str = in.readLine()) != null) {
                i++;
                System.out.println(str);
            }
            System.out.println(i);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}