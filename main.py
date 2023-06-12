#  BSD 3-clause License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE



# Jetson Nano SmartGate for Wens course - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #

#sudo pip install Jetson.GPIO


#This program was divided into 3 parts: Network communications, A.I Prediction and GPIO communications

##### Network communications#####
# We relied on Wifi encryption, instead of using our self-made encryption#
import const
import datetime

import socket
import traceback


import signet

import pred
import time


def DoTheMagic(content):
    if (const.Debug):
        start_time = time.time()
    Payload = signet.DecryptConn(recvdata)
    Is_Authorized=pred.DotheImageMagic()
    if (const.NFC):
        pass    #Do Something Here
    if (const.Debug):
        print("Response Elapsed", time.time() - start_time)
    return signet.ResponseFromRequest(Payload, Is_Authorized)

serverSocket = socket.socket()
serverSocket.bind(("0.0.0.0", const.PORT))
serverSocket.listen()

try:
    while (True):
        (clientConnection, clientAddress) = serverSocket.accept()
        recvdata=clientConnection.recv(1024).split(b'\n')[0]
        print("recvlen=",len(recvdata))
        print(("Recv", recvdata))
        response =DoTheMagic(recvdata)
        print(("sent", response))
        clientConnection.send(response+b"\n")
        clientConnection.close();
except:
    traceback.print_exc()
    serverSocket.close();