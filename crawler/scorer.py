

class Scorer:

	"""
	normalizes the scores on the scale of 0 to 1, where 1 is closes to the best score
	small_is_better decides whether the minimum score is the best or the maximum score
	"""
	@staticmethod
	def normalize(scores, small_is_better=0):
		print ('scores: ' + str(scores))
		if not scores:
			return dict([])

		vsmall = 0.00001
		min_score = min(scores.values())
		max_score = max(scores.values())

		if small_is_better:
			return dict([(url, (float(min_score)/max(vsmall, score))) for (url, score) in scores.items()])
		else:
			max_score = vsmall if(max_score==0) else max_score
			return dict([(url, (float(score)/max_score)) for (url, score) in scores.items()])


	@staticmethod
	def frequency_score(rows):
		counts = dict([(row[0], 0) for row in rows])
		for row in rows:
			counts[row[0]] += 1

		return Scorer.normalize(counts)


	"""
	returns the sum of locations for each of the urls in rows list
	the url with the lower sum implies that all the occur words
	occurred nearer to the top in that url
	"""
	@staticmethod
	def location_score(rows):
		min_locations = dict([(row[0], 1000000) for row in rows])

		for row in rows:
			min_loc = sum([int(s) for s in row[1:]])
			if(min_loc < min_locations[row[0]]):
				min_locations[row[0]] = min_loc

		return Scorer.normalize(min_locations, small_is_better = 1)




