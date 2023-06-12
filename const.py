#  BSD 3-clause License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE



# Jetson Nano SmartGate for Wens course - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #



#This program was divided into 3 parts:
# Network communications, A.I Prediction and 8266  communications
import os
##### constants #####
PRIVATE_KEY = b"1952095819520262"
Debug = True
PORT = 19520
if os.name == "posix":
    config_path = "./trained_models/"
elif os.name == "nt":
    config_path = "C:/Users/thanh/PycharmProjects/jetsonnet/trained_models/"
else:
    print("Unsupported OS")
    exit
config_file = "yolov7-tiny.cfg"
data_file = "obj.data"
weights = "yolov7-tiny_final.weights"
batch_size = 1
thresh=0.25
NFC=False