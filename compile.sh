#!/bin/bash
mkdir -p bin

#mkdir -p debug
#cd debug
#cmake -DCMAKE_BUILD_TYPE=DEBUG ..
#make
#cp src/omsimgui ../bin/omsimgui
#cd ..

mkdir -p release
cd release
cmake ..
make
cp src/omsimgui ../bin/omsimgui
cd ..

