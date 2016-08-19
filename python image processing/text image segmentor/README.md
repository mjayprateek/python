# About python text image segmentor

This image segmentor extracts images of individual characters (alphabets or numbers) 
from an image of typed and non-cursive hand-written text. These individual character images
then can be processed and used as an input for character recognition ML algorithms.

The alogrithm for extracting characters out of text is very crude and brute force. Moreover, to use these images for
some ML system, one needs to do some post-processing and normalization of the
image sizes.

## Algorithm
1. First step is to iterate through all the rows to determine which rows are empty lines or white spaces. This is done by using a threshold of some grayscale pixel value. For the image given with
the code it worked out to be 190. I achieve this threshold by zooming-in on the image
and closely looking at the pixel values of the text characters and of the whitespaces
which separate these texts. Basically, what we are doing is this: given a text_color_threshold (below which every pixel value is a text), identify the empty rows (the ones with all pixels below text_color_threshold)

2. Once the program has the indices of rows which comprises the text, it iterates over all the columns of these rows to figure out which columns of pixels can be considered as white spaces. This is achieved by comparing the percentage of text pixels present in a column with the threshold specified by text_color_per_column_percent. If the percentage of text pixels in a column is less than text_color_per_column_percent, then that column can be taken as a white space separating the chracter pixels. Once the program has the indices of all white space columns within a text row, the boundaries of such columns alongwith the empty rows is used to segment the image into individual characters.

3. usage:
 - segmentor = Segmentor(text_color_threshold=190, text_color_per_column_percent=5)
 - segmentor.segment(img_file='text_image.png', folder_path='segmented/')
