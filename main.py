import numpy as np
import cv2

import tkinter as tk
import tkinter.ttk as ttk
from tkcolorpicker import askcolor

# Load an color image in grayscale
#img = cv2.imread('kajak.jpg',1)

cap = cv2.VideoCapture(0)

first = 1
imgSize = 3;

height = 0.0
width = 0.0

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

color = askcolor((255, 255, 0), root)
colorStr = str(color)
str = colorStr.replace("(", "")
finalStr = str.replace(")", "")

vallist = [x.strip() for x in finalStr.split(',')]

vallist.pop()

print(vallist)

index = 0

'''
for x in vallist:
    count = 0
    biggest = 0
    if int(vallist[int(x)]) > biggest:
        biggest = int(vallist[int(x)])
        index = count
    count+1
'''

index = vallist.index(max(vallist))

ColerRange = int(100)

upperList = [int(vallist[0])+ColerRange,int(vallist[1])+ColerRange,int(vallist[2])+ColerRange]
lowerList = [int(vallist[0])-ColerRange,int(vallist[1])-ColerRange,int(vallist[2])-ColerRange]


# lowerBound=np.array([33,80,40])
# upperBound=np.array([102,255,255])

for n, i in enumerate(lowerList):
       if i < 0:
            lowerList[n] = 0

for n, i in enumerate(upperList):
       if i > 255:
            upperList[n] = 255

lowerBound=np.array(lowerList)
upperBound=np.array(upperList)

print(upperBound)
print(lowerBound)

while(True):


    ret, frame = cap.read()


    if (first):
        height, width = frame.shape[:2]
        #print('h:' + str(height) + 'w:' + str(width))
        first = 0

    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imgHSV, lowerBound, upperBound)

    maskNewSize = cv2.resize(mask, (int(width/imgSize), int(height/imgSize)))
    frameNewSize = cv2.resize(frame, (int(width/imgSize), int(height/imgSize)))

    im2, contours, hierarchy = cv2.findContours(maskNewSize, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frameNewSize, contours, -1, (255, 0, 0), 3)

    cv2.imshow('mask',maskNewSize)
    cv2.imshow('frame', frameNewSize)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
