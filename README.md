# PolyExtract
Extract Polygons from the image and find their area

This is the program to calculate the area of polygons extracted from the satellite image
Methods of blurring and canny edge detection are used to create a binary image of the input image and then contours are found for the image to identify polygons in the image and hence their areas. Also, it's attempted to calculate the area of the farms inside each polygons, but it's incomplete at this moment due to inaccessibility to the python package gbdxtools.

v1.3

How do I get set up?

Dependencies:

  1.opencv-python 

  2.argparse 

  3.gbdxtools


Run the program:
python main_polyExtract.py -i "PATH_TO_THE_IMAGE_FILE" 

or 

python main_polyExtract.py --image i "PATH_TO_THE_IMAGE_FILE"


# Author: 

Nikhil S Hubballi 

nikhil.hubballi@gmail.com
