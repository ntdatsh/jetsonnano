#  BSD 3-clause License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE


# Jetson Nano SmartGate for Wens course - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #
# last resort for communicating - 8266 emulation
import os
import socket
import base64
import time

##### constants #####
PRIVATE_KEY = b"1952095819520262"
Debug = True
IP="192.168.55.1"
PORT = 19520

# Crypto Functions
def CheckChecksum(content):
    if content[7] ==content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]:
        return 1
    return 0

def GenChecksum(content):
    return (content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]).to_bytes(1,'big')


def EncryptConn(content):
    privk = PRIVATE_KEY # get the private key
    tmp = os.urandom(8)  # generate 64-bit random number for IV
    if len(content) != 8:#checksum
        content+=GenChecksum(content)
    tmp = tmp+bytes(a ^ b for a, b in zip(content, tmp))
    return base64.b64encode(bytes(a ^ b for a, b in zip(privk, tmp)))


def DecryptConn(content):
    privk = PRIVATE_KEY
    content = base64.b64decode(content)
    tmp = bytes(a ^ b for a, b in zip(content, privk))
    return bytes(a ^ b for a, b in zip(tmp[0:8],tmp[8:16]))

# Communicating Functions
def PrintSB(tmp):
    for i in range(len(tmp)):
        print(int(tmp[i]),",")
    print("\n")


def BuildSB():
    tmp=b'\x01'
    tmp+=b'\x01'
    tmp+=os.urandom(1)
    tmp+=b'\x00'
    tmp += b'\x00'
    tmp += b'\x00'
    tmp += b'\x00'
    tmp+=GenChecksum(tmp)
    print("\n","build payload")
    PrintSB(tmp)
    return tmp

def Dict2Bytes(dict_val):
    tmp = dict_val["type"].to_bytes(1, 'big')
    tmp += dict_val["ID"].to_bytes(1, 'big')
    tmp += dict_val["response"]
    tmp += GenChecksum(tmp)
    return tmp


def Bytes2Dict(content):
    tmp = {"type": content[0], "ID": int.from_bytes(content[1:2], 'big'), "response": content[2:7]}
    return tmp

def Authen(content, nonce):
    if (content[0]!=2):
        print("Wrong AuthResp ")
        return 0
    if (content[1]!=0):
        print("Wrong device")
        return 0
    if (content[6]!=nonce):
        print("Wrong nonce")
        return 0
    if (CheckChecksum(content)==0):
        print("wrong checksum")
        return 0
    if (content[2]!=1):
        print("Not allowed")
        return 0
    for i in range(4):
        if (content[i+2]!=1):
            print("potential bitflip")
            return 0
    return 1
# emulation Functions

def DoDistance():
    print("Emulation: Distance 49cm - > someone in range")
    return 49 #in centimeters

def ControlLED(state, duration=0):
    if(state==1):
        print("Entrance Allowed")
    if (state==2):
        print("Please wait...")
    if (state ==3):
        print("Entrance Declined")


#
def Run():
    while (1):
        input("press enter to run simulate")
        if (DoDistance()<50):
            start_time=time.time()
            ControlLED(2)
            Conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Conn.connect((IP, PORT))
            req = BuildSB()
            nonce = req[2]
            Conn.send(EncryptConn(req)+b"\n")
            print("Data sent to server... waiting for decision")
            recvdata = Conn.recv(1024).split(b'\n')[0]
            Conn.shutdown(socket.SHUT_RDWR)
            recvdata = DecryptConn(recvdata)
            print("Received Data")
            PrintSB(recvdata)
            if(Authen(recvdata,nonce)):
                ControlLED(1)
            else:
                ControlLED(3)
            print("Takes approx.", time.time() - start_time," seconds to accomplish")

Run()









