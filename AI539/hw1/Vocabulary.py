from collections import Counter 
import operator
from re import sub, compile
import matplotlib.pyplot as plt
import numpy as np
import re

class UnimplementedFunctionError(Exception):
	pass

class Vocabulary:

	def __init__(self, corpus):

		self.word2idx, self.idx2word, self.freq = self.build_vocab(corpus)
		self.size = len(self.word2idx)

	def most_common(self, k):
		freq = sorted(self.freq.items(), key=lambda x: x[1], reverse=True)
		return [t for t,f in freq[:k]]


	def text2idx(self, text):
		tokens = self.tokenize(text)
		return [self.word2idx[t] if t in self.word2idx.keys() else self.word2idx['UNK'] for t in tokens]

	def idx2text(self, idxs):
		return [self.idx2word[i] if i in self.idx2word.keys() else 'UNK' for i in idxs]


	###########################
	## TASK 1.1           	 ##
	###########################
	def tokenize(self, text):
		"""
	    
	    tokenize takes in a string of text and returns an array of strings splitting the text into discrete tokens.

	    :params: 
	    - text: a string to be tokenize, e.g. "The blue dog jumped, but not high."

	    :returns:
	    - tokens: a list of strings derived from the text, e.g. ["the", "blue", "dog", "jumped", "but", "not", "high"] for word-level tokenization
	    
	    """ 
		# token = re.compile(r'\b\w+\b')
		# token = text.findall(text.lower())

		text_punctuation = re.sub(r'[^\w\s]','', text)		#remove punctuation 
		text_lower = text_punctuation.lower()				#convert text to lowercase
		tokens = text_lower.split() 						#split the text into tokens
  
		return tokens



  
		# REMOVE THIS ONCE YOU IMPLEMENT THIS FUNCTION
		#raise UnimplementedFunctionError("You have not yet implemented tokenize.")



	###########################
	## TASK 1.2            	 ##
	###########################
	def build_vocab(self,corpus):
		"""
	    
	    build_vocab takes in list of strings corresponding to a text corpus, tokenizes the strings, and builds a finite vocabulary

	    :params:
	    - corpus: a list string to build a vocabulary over

	    :returns: 
	    - word2idx: a dictionary mapping token strings to their numerical index in the dictionary e.g. { "dog": 0, "but":1, ..., "UNK":129}
	    - idx2word: the inverse of word2idx mapping an index in the vocabulary to its word e.g. {0: "dog", 1:"but", ..., 129:"UNK"}
	    - freq: a dictionary of words and frequency counts over the corpus (including words not in the dictionary), e.g. {"dog":102, "the": 18023, ...}

	    """ 
		word_counts = Counter()

		for text in corpus:
			tokens = self.tokenize(text)
			word_counts.update(tokens)

		# Filter words by minimum frequency
		filtered_words = {word for word, count in word_counts.items() if count >= 5} #minimum frequency 

		# Create a list of words, sorted by frequency and then alphabetically
		sorted_words = sorted(filtered_words, key=lambda word: (- word_counts[word], word))
		
		# Add 'UNK' to handle unknown words during text processing
		sorted_words.append('UNK')

		# Create word2idx and idx2word dictionaries
		word2idx = {word: idx for idx, word in enumerate(sorted_words)}
		idx2word = {idx: word for word, idx in word2idx.items()}

		return word2idx, idx2word, word_counts

		# REMOVE THIS ONCE YOU IMPLEMENT THIS FUNCTION
		#raise UnimplementedFunctionError("You have not yet implemented build_vocab.")


	###########################
	## TASK 1.3              ##
	###########################
	def make_vocab_charts(self):
		"""
	    
	    make_vocab_charts plots word frequency and cumulative coverage charts for this vocabulary. See handout for more details

	    
	    """ 
		freqs = np.array(sorted(self.freq.values(), reverse=True))

		# # token id
		# token_id = [self.word2idx[key] for key in self.freq.keys()]
        # # token_id sorted based on frequency
		# sorted_id_freq = sorted(zip(freqs, token_id), key=operator.itemgetter(0), reverse=True)
		# sorted_freq, sorted_id = zip(*sorted_id_freq)
		# cum_coverage = [sum(sorted_freq[:i + 1]) / sum(sorted_freq) for i in range(len(sorted_freq))]

		plt.figure(figsize=(12, 6))

		# Subplot 1: Frequency Distribution
		plt.subplot(1, 2, 1)
		plt.plot(freqs, label='Token Frequency')
		plt.yscale('log')  # Log scale for better visibility
		#plt.axhline(y=cut_off, color='r', linestyle='-', label='freq=50')
		plt.title('Token Frequency Distribution')
		plt.xlabel('Token Rank')
		plt.ylabel('Frequency (log scale)')
		plt.grid(True)
  
		# cutoff_index = next(idx for idx, value in enumerate(sorted_freq) if value <= cut_off)
		# cutoff_cum_coverage = round(cum_coverage[cutoff_index],2)

		# Subplot 2: Cumulative Fraction Covered
		plt.subplot(1, 2, 2)
		cumulative = np.cumsum(freqs) / np.sum(freqs)
		plt.plot(cumulative, label='Cumulative Fraction of Total Occurrences')
		plt.title('Cumulative Token Coverage')
		plt.xlabel('Token Rank')
		plt.ylabel('Fraction of Total Occurrences Covered')
		plt.grid(True)
		plt.show()
		
	    
		
     	# REMOVE THIS ONCE YOU IMPLEMENT THIS FUNCTION
		#raise UnimplementedFunctionError("You have not yet implemented make_vocab_charts.")

