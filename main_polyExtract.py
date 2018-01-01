#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 12:14:36 2017

@author: nikhil.s.hubballi
"""

# importing the packages needed
import argparse
import cv2

""" Step 1: Receive and load the image """

# argument parse 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "Provide the path to the image")
args = vars(ap.parse_args())
 
# Load the Image
assert args["image"] is not None, 'Please provide the arguments for path to the image'

image = cv2.imread(args["image"])
sizeX = image.shape[0]
sizeY = image.shape[1]

# Check for the size of the image 
if sizeY > 3000:
    fX = round(3000/sizeX, 1)
    fY = round(3000/sizeY, 1)
    pic = cv2.resize(image, (0,0), fx=fX, fy=fY)
else:
    pic = image

thumbnail = pic.copy()

cv2.imshow('image',pic) #Display data image
cv2.imwrite('thumbnail.png',pic) # Save Data image

""" Step 2 : Extract the polygons from the image """
# Apply Canny Edge Detection
smooth = cv2.GaussianBlur(pic, (3, 3), 0) #Apply the filter to remove high frequency noise in the image
edge = cv2.Canny(smooth, 170, 200) #Detects the edges in the image with values fed in (minVal & maxVal)

cv2.imshow('edges',edge) #Show image, processed for edge detection
cv2.imwrite('edged.png',edge)

# Find the contours from the image
(_, counts, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
counts = sorted(counts, key = cv2.contourArea, reverse = True)[:6]

#Draw the contours/ extracted polygons on the image    
cv2.drawContours(pic, counts, -1, (220,170,170), -1) #draws the contours on the original image


""" Step 3 : Finding the area of the extracted polygons"""   
area = [] 
for c in counts:
    temp = cv2.contourArea(c) # area of the contour/polygon extracted in the previous case
    area.append(temp)
    x,y,w,h = cv2.boundingRect(c)
    cv2.putText(pic, str(temp), (int(x+w/2), int(y+h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    

cv2.imshow('Area', pic) # Display the results, calculated area on the masks of polygons
cv2.imwrite('PolyExtractArea.png',pic)


""" Step 4 : Calculate individual farm area in a polygon (Bonus)"""
x,y,w,h = cv2.boundingRect(counts[1])
cropped = thumbnail[y:y+h, x:x+w]
# In the polygon chosen, Land use Land cover classification is to be done to
# determine the different classes and by identifying the farms using LULC, the area 
# can be calculated. I have to use a package called gbdx tools for lulc, but since 
# I was not able to import the package, I've just included the code for that step.

import gbdxtools

gbdx = gbdxtools.Interface()

lulc = gbdx.Task('lulc') # syntax referred from gbdxtools documentation
lulc.inputs.image = cropped
wf = gbdx.Workflow([lulc])
wf.savedata(lulc.outputs.image, 'lulc.png')
wf.execute()

# the result of the lulc classification will be classes (different farms) and the area
# of each classes can be calculated 

cv2.waitKey(0)
cv2.destroyAllWindows() 

# Since the resolution of the image was not known in terms of meters, only the values
# in the units of Square pixels are mentioned/shown in the results.

