from urllib.request import urlopen
from bs4 import *
from urllib.parse import urljoin
from mysql.connector import *
from db_config import *
import re
from my_wordutil import *


class crawler:
	#initialize the crawler with the name of the database

	def __init__(self, dbname):
		self.con = connect(**Config.localhost())
		self.cur = self.con.cursor(buffered = True)

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

	#Auxiliary function for getting an entry id and adding
	#it if it's not present
	def get_entry_id(self, table, field, value, createnew=True):
		#print("Table: %s, Field: %s, Value: %s" % (table, field, value))
		find_value = "select * from %s where %s = '%s'" % (table, field, value)
		insert_value = "insert into %s (%s) values ('%s')" % (table, field, value)
		
		self.cur.execute(find_value)
		res = self.cur.fetchone()

		if(res==None):
			try:
				self.cur.execute(insert_value)
				return self.cur.lastrowid
			except:
				print("Exception while inserting %s in `%s`.`%s`" %(value, table, field))
				return -1;
		
		return res[0]



	# Index an individual page
	def add_to_index(self, url, soup):

		if(self.is_indexed(url)): 
			#print("%s is indexed" %(url))
			return

		print('Indexing %s' % url)

		#get the words
		text = self.get_text_only(soup)
		words = WordUtil.separatewords(text)

		#get the url id
		urlid = self.get_entry_id('urls', 'url', url)

		if(urlid >=0):
		
			#link each word to this url
			for i in range(len(words)):
				word = words[i]

				if(word in WordUtil.ignorewords): continue

				wordid = self.get_entry_id('words', 'word', word)

				if(wordid >= 0):
					self.cur.execute("insert into word_location(url, word, location) values(%d, %d, %d)" % (urlid, wordid, i))

	

	# Extract the text from an HTML page (no tags)
	def get_text_only(self, soup):
		if(soup.html is None):
			return soup.get_text()
		else:
			return soup.html.body.get_text()


	# returns true if this url is already indexed
	def is_indexed(self, url):
		find_value = "select * from %s where %s = '%s'" % ('urls', 'url', url)
		
		self.cur.execute(find_value)
		res = self.cur.fetchone()

		if(res==None):
			return False
		else:
			print("%s is indexed"%(url))
			return True

	

	# Add a link between two pages
	def addlinkref(self, urlFrom, urlTo, linkText):
		pass

	

	# create the database tables
	def crateindextables(self):
		pass
	


	# Starting with a list of pages, do a breadth-first
	# search to the given depth, indexing pages as we go
	def crawl(self, pages, depth = 2):
		for i in range(depth):
			
			newpages = set()
			for page in pages:
				try:
					c = urlopen(page)
				except:
					print('could not open %s' % page)
					continue

				soup = BeautifulSoup(c.read())
				self.add_to_index(page, soup)

				links = soup.find_all('a')	
				for link in links:
					if('href' in dict(link.attrs)):
						url = urljoin(page, link['href'])

						if url.find("'")!=-1: continue

						#removing location portion
						url = url.split('#')[0]

						if(url[0:4]=='http' and not self.is_indexed(url)):
							newpages.add(url)

						# doubt: we are getting text even from those 
						# urls which do not have 'http' in the beginning
						
						linkText = self.get_text_only(link)
						#print("LinkText for %s : %s" % (link, linkText))
						self.addlinkref(page, url, linkText)

				self.dbcommit()

			pages = newpages




pagelist = ['http://www.cyberciti.biz/faq/python-convert-string-to-int-functions/']
my_crawler = crawler('python')
my_crawler.crawl(pagelist)








