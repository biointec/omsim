#!/bin/bash
mkdir -p build
mkdir -p bin
cd build
cmake ..
make
cp src/omsimgui ../bin/omsimgui
cd ..
