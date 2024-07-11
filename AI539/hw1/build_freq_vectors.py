
from datasets import load_dataset
from Vocabulary import Vocabulary
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from sklearn.utils.extmath import randomized_svd
import logging
import itertools
from sklearn.manifold import TSNE
from scipy.sparse import lil_matrix, csr_matrix


import random
random.seed(42)
np.random.seed(42)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class UnimplementedFunctionError(Exception):
	pass


###########################
## TASK 2.2              ##
###########################

def compute_cooccurrence_matrix(corpus, vocab):
	"""
	    
	    compute_cooccurrence_matrix takes in list of strings corresponding to a text corpus and a vocabulary of size N and returns 
	    an N x N count matrix as described in the handout. It is up to the student to define the context of a word

	    :params:
	    - corpus: a list strings corresponding to a text corpus
	    - vocab: a Vocabulary object derived from the corpus with N words

	    :returns: 
	    - C: a N x N matrix where the i,j'th entry is the co-occurrence frequency from the corpus between token i and j in the vocabulary

	    """ 
	vocab_size = vocab.size
	word2idx = vocab.word2idx
	window_size = 4
    
    # Initialize the co-occurrence matrix
	C = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    
	for text in corpus:
		tokens = vocab.tokenize(text)
		token_indices = [word2idx.get(token, word2idx['UNK']) for token in tokens]
        
        # Iterate over each word in the text
		for center_idx, word_id in enumerate(token_indices):
            # Iterate over all words within the window around the center word
			for offset in range(-window_size, window_size + 1):
				context_idx = center_idx + offset
				if context_idx < 0 or context_idx >= len(token_indices) or context_idx == center_idx:
					continue
				context_word_id = token_indices[context_idx]
				C[word_id, context_word_id] += 1

	return C
	
	# REMOVE THIS ONCE YOU IMPLEMENT THIS FUNCTION
	#raise UnimplementedFunctionError("You have not yet implemented compute_count_matrix.")
	

###########################
## TASK 2.3              ##
###########################

def compute_ppmi_matrix(corpus, vocab):
	"""
	    
	    compute_ppmi_matrix takes in list of strings corresponding to a text corpus and a vocabulary of size N and returns 
	    an N x N positive pointwise mutual information matrix as described in the handout. Use the compute_cooccurrence_matrix function. 

	    :params:
	    - corpus: a list strings corresponding to a text corpus
	    - vocab: a Vocabulary object derived from the corpus with N words

	    :returns: 
	    - PPMI: a N x N matrix where the i,j'th entry is the estimated PPMI from the corpus between token i and j in the vocabulary

	    """ 
	C = compute_cooccurrence_matrix(corpus, vocab)
	vocab_size = vocab.size
    
    # Total count of co-occurrences
	total = np.sum(C)  # Ensuring 'total' is defined by summing all entries in the matrix C
    
    # Probabilities of individual words (summing over rows for word i and columns for word j)
	word_probs_i = np.sum(C, axis=1, keepdims=True)  # Sum over columns to get P(w_i)
	word_probs_j = np.sum(C, axis=0, keepdims=True)  # Sum over rows to get P(w_j)
    
    # Avoid division by zero and log(0) by adding a small constant (smoothing)
    # Convert probabilities to float to prevent overflow in multiplication
	word_probs_i = word_probs_i.astype(np.float64)
	word_probs_j = word_probs_j.astype(np.float64)
    
    # Compute joint probability matrix for words i and j
	joint_prob = C / total
    
    # Compute marginal probabilities for words i and j
	marginal_prob_i = word_probs_i / total
	marginal_prob_j = word_probs_j / total
    
    # Calculate the PMI, using log2 and adding a small constant to the denominator to prevent log(0)
    # Clip PMI at 0 to get PPMI
	PMI = np.log2(joint_prob / (marginal_prob_i * marginal_prob_j + 1e-8) + 1e-8)
	PPMI = np.maximum(PMI, 0)
    
	return PPMI


	
	# REMOVE THIS ONCE YOU IMPLEMENT THIS FUNCTION
	#raise UnimplementedFunctionError("You have not yet implemented compute_ppmi_matrix.")


	

################################################################################################
# Main Skeleton Code Driver
################################################################################################
def main_freq():

	logging.info("Loading dataset")
	dataset = load_dataset("ag_news")
	dataset_text =  [r['text'] for r in dataset['train']]
	dataset_labels = [r['label'] for r in dataset['train']]

	cut_off=50

	logging.info("Building vocabulary")
	vocab = Vocabulary(dataset_text[:1000])
	vocab.make_vocab_charts() 		
	plt.close()
	plt.pause(0.01)
 
	#vocab with best threshold identified from the plots
	#vocab = Vocabulary(dataset_text,cut_off)


	logging.info("Computing PPMI matrix")
	PPMI = compute_ppmi_matrix( [doc['text'] for doc in dataset['train']], vocab)


	logging.info("Performing Truncated SVD to reduce dimensionality")
	word_vectors = dim_reduce(PPMI)


	logging.info("Preparing T-SNE plot")
	plot_word_vectors_tsne(word_vectors, vocab)


def dim_reduce(PPMI, k=16):
	U, Sigma, VT = randomized_svd(PPMI, n_components=k, n_iter=10, random_state=42)
	SqrtSigma = np.sqrt(Sigma)[np.newaxis,:]

	U = U*SqrtSigma
	V = VT.T*SqrtSigma

	word_vectors = np.concatenate( (U, V), axis=1) 
	word_vectors = word_vectors / np.linalg.norm(word_vectors, axis=1)[:,np.newaxis]

	return word_vectors


def plot_word_vectors_tsne(word_vectors, vocab):
	coords = TSNE(metric="cosine", perplexity=50, random_state=42).fit_transform(word_vectors)

	plt.cla()
	top_word_idx = vocab.text2idx(" ".join(vocab.most_common(1000)))
	plt.plot(coords[top_word_idx,0], coords[top_word_idx,1], 'o', markerfacecolor='none', markeredgecolor='k', alpha=0.5, markersize=3)

	for i in tqdm(top_word_idx):
		plt.annotate(vocab.idx2text([i])[0],
			xy=(coords[i,0],coords[i,1]),
			xytext=(5, 2),
			textcoords='offset points',
			ha='right',
			va='bottom',
			fontsize=5)
	plt.show()


if __name__ == "__main__":
    main_freq()

