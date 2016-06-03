import re

class WordUtil:
	# a list of words to ignore
	ignorewords = set(['the', 'of', 'to', 'and', 'a', 'an', 'as', 'is', 'in', 'it', 'from'])


	# Separate the words by any non-whitespace character
	@staticmethod
	def separatewords(text):
		separator = re.compile(r'\W+')
		return [s.lower() for s in separator.split(text) if s!='']


	
