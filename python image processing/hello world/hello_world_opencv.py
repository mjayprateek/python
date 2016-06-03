import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('text_image.png',0)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# making a single tuple out of the img shape tuple
print 'image array size: {0}'.format(img.shape) 

print 'image number of rows: {0}'.format(len(img))

print 'image pixel column length: {0}'.format(len(img[0]))

#print 'image pixel row 0: {0}'.format(img[0])

#print 'image pixel row 15: {0}'.format(img[14])

print 'image pixel value: {0}'.format(img.item(0,0))

print 'image pixel value: {0}'.format(img[0,0])

print 'image size: {0}'.format(img.size)

print 'image dtype: {0}'.format(img.dtype)
