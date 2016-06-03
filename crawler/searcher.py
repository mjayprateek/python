from mysql.connector import *
from my_wordutil import *
from db_config import *
from importlib import *
import scorer
import sys

class searcher:
	def __init__(self, dbname):
		self.con = connect(**Config.localhost())
		self.cur = self.con.cursor()

	def __del__(self):
		self.con.close()

	def get_match_rows(self, q):
		qwords = WordUtil.separatewords(q)
		print("separated words " + str(qwords))

		return self.find_urls_matching(qwords)


	def find_urls_matching(self, qwords):
		select_term_const = 'SELECT w0.url '
		from_term_const = ' FROM '
		where_term_const = ' WHERE '
		
		select_term = select_term_const
		from_term = from_term_const
		where_term = where_term_const
		wordids = []
		rows = []


		# final search term will have a form like select w0.url, w0.location, w1.location, w2.location, ....
		incremental_select_term = ", w%d.location "
		
		# incremental from term will have a form like 
		# from word_location w0 join word d0 on w0.word = d0.id and d0.word = 'word1', 
		# word_location w1 join word d1 on w1.word = d1.id and d1.word = 'word2'
		incremental_from_term = "word_location w%d JOIN words d%d ON w%d.word = d%d.id AND d%d.word = '%s' "

		# incremental_where_term will have a form like this: w0.url = w1.url and w1.url = w2.url and ....
		incremental_where_term = " w%d.url = w%d.url "

		for (i, word) in enumerate(qwords):
			if(word in WordUtil.ignorewords):
				continue

			self.cur.execute("select id from words where word = '%s' " % (word))
			wordrow = self.cur.fetchone()
			if(wordrow!=None):
				wordids.append(wordrow[0])

			
			select_term = select_term + (incremental_select_term % (i))
			from_term = from_term + self.prefix(i, ', ') + (incremental_from_term % (i, i, i, i, i, word))
			where_term = where_term + ('' if (where_term==' WHERE ') else ' AND ') + ((incremental_where_term % (0,i)) if i>0 else '')



		if(select_term==select_term_const):
			return [], wordids


		search_query = select_term + from_term + where_term
			
		print("search query : " + search_query)

		self.cur.execute(search_query)
		res = self.cur.fetchall()

		if(res!=None):
			print("rows: " + str(len(res))) 
			rows = [row for row in res]

		return rows, wordids


	def prefix(self, i, prefix):
		return prefix if i>0 else ''



	def get_scored_list(self, rows, wordids):
		total_scores = dict([(row[0], 0) for row in rows])

		#scoring functions will be put here later
		#weights = [(1.0, scorer.Scorer.frequency_score(rows))]
		weights = [(1.0, scorer.Scorer.location_score(rows))]

		for(weight, scores) in weights:
			for url in total_scores:
				total_scores[url] += weight*scores[url]

		return total_scores


	def get_url_name(self, id):
		self.cur.execute(("select url from urls where id=%d")%(id))
		return self.cur.fetchone()[0]


	def query(self, q):
		rows, wordids = self.get_match_rows(q)
		scores = self.get_scored_list(rows, wordids)
		ranked_scores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)

		for (score, url) in ranked_scores:
			print( '%f \t %s' % (score, self.get_url_name(url)))


def search():
	my_searcher = searcher('python')
	my_searcher.query('string to int in python')


if __name__ == "__main__":
	print ('running in command line. Reloading modules')
	reload(scorer)
	search()
else:
	print ('running from another module: ' + __name__)


