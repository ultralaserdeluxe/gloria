#!/usr/bin/env python
import numpy as np
import cv2
import time

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares
def removeLargeSquares(squares,width,height):
    temp=[]
    for element in squares:
        squareWidth=element[2][0]-element[0][0]
        squareHeight=element[2][1]-element[0][1]
        if squareHeight*squareWidth<((width*height)/4):
            temp.append(element)
            
    return temp
def removeMultipleSquares(squares):
    temp=[]
    toReturn=[]        
    for element in squares:
        minHeight=1921
        maxHeight=0
        minWidth=1081
        maxWidth=0
        for i in range(4):
            if element[i][0]<minWidth:
                minWidth=element[i][0]
            if element[i][0]>maxWidth:
                maxWidth=element[i][0]
            if element[i][1]<minHeight:
                minHeight=element[i][1]
            if element[i][1]>maxHeight:
                maxHeight=element[i][1]
        centerWidth=minWidth+(maxWidth-minWidth)/2
        centerHeight=minHeight+(maxHeight-minHeight)/2
        var=True
        for center in temp:
            if minWidth<center[0] and maxWidth>center[0] and minHeight<center[1] and maxHeight>center[1]:
                var=False
        if var:
            temp.append((centerWidth,centerHeight))
            toReturn.append(element)
    return toReturn,temp
def filter(squares,centerpoints):
    if len(centerpoints)>10:
        del centerpoints[0]
    toReturn=[]
    for element in squares:
        rating=0
        minHeight=1921
        maxHeight=0
        minWidth=1081
        maxWidth=0
        for i in range(4):
            if element[i][0]<minWidth:
                minWidth=element[i][0]
            if element[i][0]>maxWidth:
                maxWidth=element[i][0]
            if element[i][1]<minHeight:
                minHeight=element[i][1]
            if element[i][1]>maxHeight:
                maxHeight=element[i][1]
        centerWidth=minWidth+(maxWidth-minWidth)/2
        centerHeight=minHeight+(maxHeight-minHeight)/2
        if len(centerpoints)>9:
            for subelement in centerpoints:
                center=subelement[0]
                if ((minWidth<center[0]) and (maxWidth>center[0]) and (minHeight<center[1]) and (maxHeight>center[1])):
                    rating=rating+1
            if rating>4:
                toReturn.append(element)
    return toReturn
def clearBuffer(cap):
    tid=time.time()
    while True:
        ret, img = cap.read()
        if time.time()-tid>0.20:
            break
        tid=time.time()
    

if __name__ == '__main__':
    from glob import glob
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("tcp://192.168.99.1:5000?resolution=752x416.mjpg")
    ret, img = cap.read()
    height, width, depth = img.shape
    centerpoints=[]
    while True:
        clearBuffer(cap)
        ret, img = cap.read()
        squares = find_squares(img)
        squares=removeLargeSquares(squares,width,height)
        squares,centerPointsFromIteration=removeMultipleSquares(squares)
        if centerPointsFromIteration:
            centerpoints.append(centerPointsFromIteration)
        squares=filter(squares,centerpoints)
        
        #print("squares")
        #print(squares)
        cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        cv2.imshow('squares', img)
        cv2.waitKey(1)
        #ch = 0xFF & cv2.waitKey()
        #if ch == 27:
        #    break
    cv2.destroyAllWindows()
