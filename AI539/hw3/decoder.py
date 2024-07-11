######################################################
# Use these package versions
#!pip install torchtext==0.6.0 torch==1.13.1
######################################################

import os
os.environ['CUBLAS_WORKSPACE_CONFIG'] =':16:8' #This is a command to reduce non-deterministic behavior in CUDA
import warnings
warnings.simplefilter("ignore", UserWarning)
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchtext.data import get_tokenizer
import sys
import argparse
from LanguageModel import LanguageModel
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def main():
  chkpt = "got_language_model"

  dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  logging.info('Using device: {}'.format(dev))

  logging.info("Loading tokenizer and vocab from vocab.pkl")
  text_field = pickle.load(open("vocab.pkl", "rb"))
  vocab_size = len(text_field.vocab.itos)

  logging.info("Loading checkpoint {}".format(chkpt))
  lm = LanguageModel(vocab_size).to(dev)
  #lm.load_state_dict(torch.load(chkpt))  # getting runtime error
  lm.load_state_dict(torch.load(chkpt,map_location=torch.device('cpu')))

  lm.eval()

  p = "the night is dark and full of terrors"

  # Part1
  # p_tokens = text_field.process([text_field.tokenize(p.lower)])
  # print(p_tokens.squeeze())
  # print(reverseNumeralize(p_token.squeeze(), text_field))


  # Torch is a bit frustrating at times and some things that ought to be deterministic are not.
  # This is an attempt to resolve that, but it doesn't work 100% of the time
  torch.use_deterministic_algorithms(True)
  seed = 42
  mlen = 150

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(1) Vanilla Sampling -----------")
  print(sample(lm, text_field, prompt=p, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-------(2) Temp-Scaled Sampling 0.0001 -------")
  print(sample(lm, text_field, prompt=p, temp=0.0001, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-------(3) Temp-Scaled Sampling 100 --------")
  print(sample(lm, text_field, prompt=p, temp=100, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(4) Top-k Sampling 1 -----------")
  print(sample(lm, text_field, prompt=p, k=1, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(5) Top-k Sampling 20 -----------")
  print(sample(lm, text_field, prompt=p, k=20, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(6) Top-p Sampling 0.001 -----------")
  print(sample(lm, text_field, prompt=p, p=0.001, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(7) Top-p Sampling 0.75 -----------")
  print(sample(lm, text_field, prompt=p, p=0.75, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n-----------(8) Top-p Sampling 1 -----------")
  print(sample(lm, text_field, prompt=p, p=1, max_len=mlen))


  torch.manual_seed(seed); np.random.seed(seed)
  print("\n----------- Beam Search B=1 -----------")
  print(beamsearch(lm, text_field, prompt=p, beams=1, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n----------- Beam Search B=10 -----------")
  print(beamsearch(lm, text_field, prompt=p, beams=10, max_len=mlen))

  torch.manual_seed(seed); np.random.seed(seed)
  print("\n----------- Beam Search B=50 -----------")
  print(beamsearch(lm, text_field, prompt=p, beams=50, max_len=mlen))

  print()

############################################################################################
# TASK 2.1 - Implement Beam Search
############################################################################################

def beamsearch(model, text_field, beams=5, prompt="", max_len=50):

  #device setting
  device = next(model.parameters()).device
  p_tokens = text_field.process([text_field.tokenize(prompt.lower())])
  h = torch.zeros(model.rnn.num_layers, 1, model.hidden_size).to(device)
  c = torch.zeros(model.rnn.num_layers, 1, model.hidden_size).to(device)
  s, h, c = model(p_tokens, h, c)
  log_prob, indices= torch.topk(torch.log_softmax(s[-1],dim=-1), k=beams)

  beams_states = [{"hidden":h, "cell": c, "output_tokens": indices[:,i],
         "sequence": indices[:,i],
         "log_prob": torch.tensor(0)} for i in range(beams)]

  output_beams=[]
  max_len = max_len - len(p_tokens)

  with torch.no_grad():
    for t in range(max_len):
      new_beams = []
      for beam in beams_states:
        hidden = beam["hidden"]
        cell = beam["cell"]
        sequence = beam["sequence"]
        output_tokens = beam["output_tokens"]
        scores, hidden, cell = model(output_tokens.view(1,1), hidden, cell)
        log_probs = torch.log_softmax(scores[-1], dim=-1)
        top_log_probs, top_indices = torch.topk(log_probs, k=beams)
        for log_prob, index in zip(top_log_probs[0,:], top_indices[0,:]):

          new_beam = {"hidden": hidden, "cell": cell,"output_tokens": index,
                      "sequence":torch.cat([sequence, index.view(1,)], dim=0),
                      "log_prob": beam["log_prob"] + log_prob}
          new_beams.append(new_beam)
      beams_states = sorted(new_beams, key=lambda x: x["log_prob"], reverse=True)[:beams]

      # EOS 
      if all([beam["output_tokens"] == text_field.eos_token for beam in beams_states]):
        print("EOS Found")
        break

      for x in beams_states:
        if t == max_len - 1 :
          output_beams.append(x)
        else:
          if x["output_tokens"] == text_field.eos_token:
            output_beams.append(x)

    # select best beam
    best_beam = output_beams[0]
    top_probab = best_beam["log_prob"]/len(best_beam['sequence'])
    for k in output_beams:
      if k["log_prob"]/len(k["sequence"]) > top_probab:
        best_beam = k

    decoded = reverseNumeralize(best_beam["sequence"], text_field)
    decodedString = prompt+decoded

    return decodedString
    

############################################################################################
# TASK 1.1  - implement vanilla, emterature-scaled, top-k, top-p sampling
############################################################################################

def sample(model, text_field, prompt="", max_len=50, temp=1.0, k=0, p=1):
    assert (k == 0 or p == 1), "Cannot combine top-k and top-p sampling"

    # device setup, initialize
    device = next(model.parameters()).device
    with torch.no_grad():
      p_tokens = text_field.process([text_field.tokenize(prompt.lower())])
      h = torch.zeros(model.rnn.num_layers,1,model.hidden_size).to(device)   # hidden
      c = torch.zeros(model.rnn.num_layers,1,model.hidden_size).to(device)   # cell
      s, h, c = model(p_tokens, h, c)
      output = []

      for _ in range(max_len):
        probability = torch.softmax(s[-1]/temp, dim=-1)
        
        # top-k sampling
        if k > 0:
          top_k_prob, top_k_indices = torch.topk(probability[-1], k)
          token = torch.distributions.Categorical(top_k_prob).sample()
          token = top_k_indices[token]

        # top-p sampling
        elif p < 1:
          sorted_prob, sorted_indices = torch.sort(probability[-1], descending=True)
          cumulative_prob = torch.cumsum(sorted_prob, dim=-1)
          mask = cumulative_prob < p
          mask[1:] = mask[:-1].clone()
          mask[0] = True
          token = sorted_indices[torch.distributions.Categorical(sorted_prob[mask]).sample()]

        # vanila sampling
        else:
          token = torch.distributions.Categorical(probability).sample()

        s, h, c = model(token.view(1,1), h, c)
        output.append(token)
        if token == text_field.eos_token:
          break
        decoded = reverseNumeralize(output, text_field)

        decodedString = prompt+decoded

    return decodedString


def reverseNumeralize(numeralized_string, text_field):
  strings = [text_field.vocab.itos[i] for i in numeralized_string]
  return " ".join(strings)

## Run by GPU
if __name__ == "__main__":
  main()
