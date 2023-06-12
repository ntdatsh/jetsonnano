#  BSD 3-clause License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link
#  https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE


# Jetson Nano SmartGate for Wens course@UIT - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# SIGNET - SIGnal over NETwork#
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #

# Packet:
# 1. Establish connection ( for Confidental, Integrity and Authentication purpose)
# 1.1
# 2.
# Packet include 16 bytes
# To avoid cryptanalyst from using same private key, we use a random IV and xor with the payload.
# Then we XOR them all with private key
# |IV ( 8 bytes random)| Type of Packet (1 bytes)| ID of sent packet device (essp8266) (1bytes - 254 devices, server ID =0)|
# | content (5 bytes) | checksum ( exclude the IV, by XORed them byte-by-byte)|
#type of Packet: 1: Request Auth; 2: ResponseAuth
#Content: x means different than 0 [x][][][][0]: From the Client Ultrasound
#[a][a][b][c][x]: From the Client other devices(NFC...)
#[1][1][1][1][x]: From the Server accept
#[0][0][0][0][x]: from the Server reject

import socket
import os
import const
import base64
if (const.NFC):
    #from __future__ import print_function
    #from pyrad.client import Client
    #from pyrad.dictionary import Dictionary
    import pyrad.packet
def  Authen_RADIUS(val):
    Somehow=0
    Prototype=1
    return(True)
def Prototype_NFC(NFC_ID):
    if Authen_RADIUS(NFC_ID):
        return True
    return False

def Dict2Bytes(dict_val):
    tmp = dict_val["type"].to_bytes(1, 'big')
    tmp += dict_val["ID"].to_bytes(1, 'big')
    tmp += dict_val["response"]
    tmp += GenChecksum(tmp)
    return tmp
    
def Bytes2Dict(content):
    tmp = {"type": content[0], "ID": int.from_bytes(content[1:2],'big'), "response": content[2:7]}
    return tmp

def CheckChecksum(content):
    if len(content) != 8:
        raise Exception("invalid content for check-checksum")
    if content[7] ==content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]:
        return 1
    return 0

def GenChecksum(content):
    return (content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]).to_bytes(1,'big')


def EncryptConn(content):
    privk = const.PRIVATE_KEY # get the private key
    tmp = os.urandom(8)  # generate 64-bit random number for IV
    # make sure the content have 8 bytes length
    print("enc1",content)
    print(len(content))
    if len(content) != 8:#checksum
        content+=GenChecksum(content)
    tmp = tmp+bytes(a ^ b for a, b in zip(content, tmp))
    print("enctmp", tmp)
    tmp1 = bytes(a ^ b for a, b in zip(privk, tmp))
    print("enctmp1", tmp1)
    tmp2 = base64.b64encode(tmp1)
    print("enctmp2", tmp2)
    return tmp2


def DecryptConn(content):
    privk = const.PRIVATE_KEY
    content = base64.b64decode(content)
    tmp = bytes(a ^ b for a, b in zip(content, privk))
    tmp1 = bytes(a ^ b for a, b in zip(tmp[0:8],tmp[8:16]))
    print(print("dec2", tmp1))
    return tmp1


def ResponseFromRequest(Recv, Accept):  # asume we have payload from the client, we modify it
    Answer = Accept
    content = Recv
    if (Accept !=1):
        Answer = int.to_bytes(0,1,'big')
    else:
        Answer = int.to_bytes(1,1,'big')
    if (len(content) == 16):  # case we not decrypted
        content = DecryptConn(content)
        content = content[8:16]
    tmp=b'\x02' #response Auth
    tmp+=b'\x00'#server
    for i in range(4):
        tmp += Answer
    if (content[6]==0): # case  ultrasonic
        tmp += content[2].to_bytes(1,'little') # nonce
    else:
        tmp +=content[6].to_bytes(1,'little') # if other authenticate measure
    return EncryptConn(tmp)

