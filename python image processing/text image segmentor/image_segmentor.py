"""
Algorithm:

This image segmentor is intended to separate individual text characters 
from the image of hand-written texts. These individual character images
then can be processed and used for hand-written characters recognition

1) collect the minimum pixel value for each row

2) Given a text_color_threshold (below which every pixel value is a text), identify
the empty rows (the ones with all pixels below text_color_threshold)

3) Then, iterate over all columns, over each pair of rows with 
length > 1 (that will ensure we are not going through empty rows). Collect those
column indices for which percentage of text pixels is less than text_color_per_column_percent 
within given pair of rows are white. The boundaries of such columns alongwith the empty rows 
will be used to segment the images


2) usage:
segmentor = Segmentor(text_color_threshold=190, text_color_per_column_percent=5)
segmentor.segment(img_file='text_image.png', folder_path='segmented/')


"""


import numpy as np
import cv2 as cv
import os
import os.path


class Segmentor:

	def __init__(self, text_color_threshold, text_color_per_column_percent):
		self.text_color_threshold = text_color_threshold
		self.text_color_per_column_percent = text_color_per_column_percent

	def segment(self, img_file, folder_path):

		img = cv.imread(img_file,0)
		if(not os.path.exists(folder_path)):
			os.makedirs(folder_path)

		"""
		iterating through all the rows to determine
		which rows are empty lines or white spaces
		"""
		row_wise_min_values = np.amin(img, axis=1)
		#print 'sum of pixel rows {0}'.format(row_wise_min_values)
		# print 'max possible totalfor a white row {0}'.format(255*img.shape[1])
		# print 'white percent array {0}'.format((100*row_wise_min_values)/(255*img.shape[1]) >= self.text_color_threshold )

		whitespace_row_indices = np.where(row_wise_min_values >= self.text_color_threshold)[0]
		#print 'row indices for empty lines: {0}'.format(whitespace_row_indices)

		"""
		for every pair of rows in the whitespace row indices,
		iterate over columns to find the minimum
		"""

		character_row_gaps = []
		
		for startrow, endrow in zip(whitespace_row_indices[:-1], whitespace_row_indices[1:]):
			# print 'startrow: {0} endrow: {1}'.format(startrow, endrow)
			column_wise_list = []

			if(startrow==endrow-1): continue

			continuous_white_columns_start = -1;
			started = False
			for col in  xrange(img.shape[1]):
				# print 'processing chars for row {0}'.format(row)
				started = False
				total_pixels_with_text = 0;
				
				#print 'processing chars for between {0} and {1}'.format(startrow, endrow)
				for row in xrange(startrow+1, endrow):
					if(img[row][col] < self.text_color_threshold):
						total_pixels_with_text+=1

				#print 'total pixels with text: %d and rows: %d and percent: %d' %(float(total_pixels_with_text), 
				#	float(endrow-startrow-1), float(total_pixels_with_text*100/(endrow-startrow-1)))
				
				if(float(total_pixels_with_text*100/(endrow-startrow-1)) < self.text_color_per_column_percent):
					if (not started): 
						started = True
						continuous_white_columns_start = col

				else:
					started = False
					
					if(continuous_white_columns_start>0 and col>1):
						column_wise_list.append((continuous_white_columns_start, col-1))
					
					continuous_white_columns_start = 0


			for x,y in  zip(column_wise_list[:-1], column_wise_list[1:]):
				char_img = img[startrow:endrow, x[1]:y[0]]
				filename = folder_path + 'char_at_{0}_{1}_{2}_{3}.jpg'.format(startrow-2, endrow+2, 
					x[1]-((x[1]-x[0])/2), 
					y[0] + ((y[1]-y[0])/2))
				#print filename
				cv.imwrite(filename, char_img)

			
			character_row_gaps.append(column_wise_list)



segmentor = Segmentor(text_color_threshold=190, text_color_per_column_percent=5)
segmentor.segment(img_file='text_image.png', folder_path='segmented2/')























