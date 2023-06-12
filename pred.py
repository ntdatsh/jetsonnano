#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE


# Jetson Nano SmartGate for Wens course@UIT - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# PRED - PREDict Component #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #


import cv2
import darknet
import const
import time
#init the model
nconfig_file =  const.config_path + const.config_file
ndata_file=  const.config_path + const.data_file
nweights =  const.config_path + const.weights
thresh=const.thresh
network, class_names, class_colors = darknet.load_network(
    nconfig_file,
    ndata_file,
    nweights,
    batch_size=const.batch_size
)
#init the cam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_EXPOSURE, 0.75)
#camera should be ready
time.sleep(3)
ret, frame = cap.read()
time.sleep(1)
ret, frame = cap.read()
#timestr = "START"+time.strftime("%Y%m%d-%H%M%S") + ".jpg"
#cv2.imwrite(timestr, frame)


def ReadCam(mode):
    start_time = time.time()
    ret, frame = cap.read()
    #in case LINUX camera tooo dark
    if (mode==1):
        time.sleep(2)
        ret, frame = cap.read()
    if not ret:
        raise Exception("No frame")
    timestr = time.strftime("%Y%m%d-%H%M%S-raw") + ".jpg"
    cv2.imwrite(timestr, frame)
    #cap.release()
    print("Thoi gian camera chup anh:",time.time() - start_time )
    return frame
def image_detection(cammode=0):
    image = ReadCam(cammode)
    start_time = time.time()
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    print("_____---Detect---_____", detections)
    darknet.free_image(darknet_image)
    timestr = time.strftime("%Y%m%d-%H%M%S-detection") + ".jpg"
    cv2.imwrite(timestr, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    print("Thoi gian Darknet nhan dien:", time.time() - start_time)
    print("Da ghi file anh log")
    return detections

def Chay():
    print("19520543 Nguyen Gia Hieu")
    print("19521339 Nguyen Thanh Dat")
    allow=1 #
    a=image_detection()
    if (len(a) < 1):
        for i in range(3):
            a=image_detection(1)
            if len(a)>0:
                break
    for i in range(len(a)):
        if (a[i][0]=="without_mask"):
            print("It nhat mot nguoi khong deo khau trang")
            allow=2
            return allow
        if (a[i][0]=="mask_weared_incorrect"):
            print("It nhat mot nguoi deo sai khau trang")
            allow = 3
            return allow
    if len(a)==0:
        print("Khong nhan dien duoc khuon mat")
        allow = 4
        return allow
    print("Co khau trang. Cho phep")
    return allow




