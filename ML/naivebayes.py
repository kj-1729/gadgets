# -*- coding: shift_jis -*-
import math
import sys

#import morphological
import mecab

def getwords(doc):
	result = mecab.parse(doc)
	if result is None:
		return None
	keywords = []
	for res in result:
		keywords.append(res[0])
	return keywords

class NaiveBayes:
	def __init__(self):
		self.vocabularies = set() # set of words
		self.wordcount = {}	   # {category : { words : n, ...}}
		self.catcount = {}		# {category : n}

	###########################################################################
	#                                                                         #
	#                                                                         #
	#                           API                                           #
	#                                                                         #
	#                                                                         #
	###########################################################################

	###############################################################
	#                                                             #
	#                                                             #
	#          Training Functions                                 #
	#                                                             #
	#                                                             #
	###############################################################
	
	### input training data (document)
	def train(self, doc, cat):
		word = getwords(doc)
		if word is None:
			return
		for w in word:
			self.wordcountup(w, cat)
		self.catcountup(cat)

	### input training data (document already parsed)
	def train_words(self, word, cat):
		if word is None:
			return
		for w in word:
			self.wordcountup(w, cat)
		self.catcountup(cat)

	###############################################################
	#                                                             #
	#                                                             #
	#        Classification Functions                             #
	#                                                             #
	#                                                             #
	###############################################################
	
	### based on the trained algorithm, and a document,
	### find the best matching category to this doc.
	def classifier(self, doc):
		best = None # best category
		max = -sys.maxint
		word = getwords(doc)
		if word is None:
			return None
		
		# calculate log(prob) by category
		for cat in self.catcount.keys():
			prob = self.score(word, cat)
			if prob > max:
				max = prob
				best = cat

		return best

	### classifier (input: document already parsed)
	def classifier_words(self, word):
		best = None # best category
		max = -sys.maxint
		if word is None:
			return None
		
		# calculate log(prob) by category
		for cat in self.catcount.keys():
			prob = self.score(word, cat)
			if prob > max:
				max = prob
				best = cat

		return best

	###############################################################
	#                                                             #
	#                                                             #
	#           Calc Posterior Probability for a doc              #
	#                                                             #
	#                                                             #
	###############################################################
	
	### calculate posterior probability distribution by category
	### given trained algorithm & a document
	### --------------------------------------------------------
	### input: document
	### output: [Pr(cat_1|doc), Pr(cat_2|doc), ..., Pr(cat_n|doc)]
	def posterior(self, doc):
		word = getwords(doc)
		if word is None:
			return None
		
		# calculate log(prob) by category
		sumprob = 0
		posterior = {}
		cnt = len(self.catcount.keys())
		
		padding = 0
		for cat in self.catcount.keys():
			scr = self.score(word, cat)
			padding -= scr
		padding /= cnt
		
		for cat in self.catcount.keys():
			scr = self.score(word, cat) + padding
			prob = math.exp(scr)
			#print "in posterior: ", cat, ": (", scr, ", ", prob, ")"
			posterior[cat] = prob
			sumprob += prob
		
		if sumprob < 0.00000001:
			return None
		
		for cat in self.catcount.keys():
			posterior[cat] /= sumprob
		
		return posterior

	### calculate posterior probability distribution by category
	### given trained algorithm & a document (already parsed)
	### --------------------------------------------------------
	### input: word list of the doc
	### output: [Pr(cat_1|doc), Pr(cat_2|doc), ..., Pr(cat_n|doc)]
	def posterior_words(self, word):
		if word is None:
			return None
		
		# calculate log(prob) by category
		sumprob = 0
		posterior = {}
		cnt = len(self.catcount.keys())
		
		padding = 0
		for cat in self.catcount.keys():
			scr = self.score(word, cat)
			padding -= scr
		padding /= cnt
		
		for cat in self.catcount.keys():
			scr = self.score(word, cat) + padding
			prob = math.exp(scr)
			#print "in posterior_words: cat=", cat, ": (scr, prob) = (", scr, ", ", prob, ")"
			posterior[cat] = prob
			sumprob += prob
		
		if sumprob < 0.00000001:
			return None
		
		for cat in self.catcount.keys():
			posterior[cat] /= sumprob
		
		return posterior
	
	
	###########################################################################
	#                                                                         #
	#                                                                         #
	#              Help Functions                                             #
	#                                                                         #
	#                                                                         #
	###########################################################################

	def wordcountup(self, word, cat):
		self.wordcount.setdefault(cat, {})
		self.wordcount[cat].setdefault(word, 0)
		self.wordcount[cat][word] += 1
		self.vocabularies.add(word)

	def catcountup(self, cat):
		self.catcount.setdefault(cat, 0)
		self.catcount[cat] += 1

	def score(self, word, cat):
		score = math.log(self.priorprob(cat))
		for w in word:
			score += math.log(self.wordprob(w, cat))
		return score

	def priorprob(self, cat):
		return float(self.catcount[cat]) / sum(self.catcount.values())

	def incategory(self, word, cat):
		# returns the number of occurrence in a category
		if word in self.wordcount[cat]:
			return float(self.wordcount[cat][word])
		return 0.0

	def wordprob(self, word, cat):
		# calc P(word|cat)
		prob = \
			(self.incategory(word, cat) + 1.0) / \
				  (sum(self.wordcount[cat].values()) + \
				   len(self.vocabularies) * 1.0)
		return prob

	#def printwords(self, kw, cat):
	def printwords(self, doc, cat):
		word = getwords(doc)
		if word is None:
			return
		for k in word:
			print k+'|',
		print ' => '+cat

	def getcategorylist():
		return wordcount.keys

