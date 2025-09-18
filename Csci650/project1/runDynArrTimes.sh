#!/bin/bash

#bash script to generate data and make plots for dynamic array times
make #g++ -std=c++11 dynamic_array.cpp -o runDynArr.out
./runDynArr.out | python3 plotDynArrData.py
