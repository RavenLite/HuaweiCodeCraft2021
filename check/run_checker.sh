#!/bin/bash

curl -X POST -H "Content-Type: application/json" \
        -d '{"msg_type":"text","content":{"text":"request example"}}' \
  https://open.feishu.cn/open-apis/bot/v2/hook/816fb57f-3caa-4f67-92f3-5757bb7a0c58 

cppname=main.cpp
outname=${cppname%.*}
outname=$outname".out"
g++ $cppname -o $outname
./$outname