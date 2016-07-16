# About python text image segmentor

This image segmentor is intended to separate individual text characters 
from the image of hand-written/typed texts. These individual character images
then can be processed and used for hand-written characters recognition.

The alogrithm is very crude and brute force. Moreover, to use these images for
some ML system, one needs to do some post-processing and normalization of the
image sizes.

## Algorithm
1. First step is to iterate through all the rows to determine which rows are empty lines or white spaces. This is done by using a threshold of some grayscale pixel value. For the image given with
the code it worked out to be 190. I achieve this threshold by zooming-in on the image
and closely looking at the pixel values of the text characters and of the whitespaces
which separate these texts. Basically, what we are doing is this: given a text_color_threshold (below which every pixel value is a text), identify the empty rows (the ones with all pixels below text_color_threshold)

2. Then, iterate over all columns, over each pair of rows with 
length > 1 (that will ensure we are not going through empty rows). Collect those
column indices for which percentage of text pixels is less than text_color_per_column_percent 
within given pair of rows are white. The boundaries of such columns alongwith the empty rows 
will be used to segment the images

3. usage:
 - segmentor = Segmentor(text_color_threshold=190, text_color_per_column_percent=5)
 - segmentor.segment(img_file='text_image.png', folder_path='segmented/')
