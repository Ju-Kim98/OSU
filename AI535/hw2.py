"""
CIFAR Image Classification using Fully-Connected Network 
JuHyun Kim
"""

from turtle import width
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
font = {'weight' : 'normal','size'   : 22}
matplotlib.rc('font', **font)
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')



######################################################
# Q1 Implement Init, Forward, and Backward For Layers
######################################################


class SigmoidCrossEntropy:
  
    def forward(self, logits, labels):
        self.sigmoid_output = 1 / (1 + np.exp(-logits))
        loss = -np.mean(labels * np.log(self.sigmoid_output + 1e-7) + (1 - labels) * np.log(1 - self.sigmoid_output + 1e-7))
        return loss

    def backward(self, logits, labels):
        grad = self.sigmoid_output - labels
        return grad



class ReLU:
    def forward(self, input):
        self.input = input  
        return np.maximum(0, input)
      
    def backward(self, grad):
        return grad * (self.input > 0).astype(grad.dtype)

    # No parameters so nothing to do during a gradient descent step
    def step(self, step_size, momentum=0, weight_decay=0):
        return



class LinearLayer:

  # TODO: Initialize our layer with (input_dim, output_dim) weight matrix and a (1,output_dim) bias vector
  def __init__(self, input_dim, output_dim):
        # He initialization for weights
        self.weights = np.random.randn(input_dim, output_dim) * np.sqrt(2. / input_dim)
        self.bias = np.zeros((1, output_dim))
        self.velocity_weights = np.zeros_like(self.weights)
        self.velocity_bias = np.zeros_like(self.bias)
  # TODO: During the forward pass, we simply compute XW+b
  def forward(self, input):
    self.input = input
    output = np.dot(input, self.weights) + self.bias
    return output
  def backward(self, grad):
    self.grad_weights = np.dot(self.input.T, grad)
    self.grad_bias = np.sum(grad, axis=0, keepdims=True)
    grad_input = np.dot(grad, self.weights.T)
    return grad_input

  ######################################################
  # Q2 Implement SGD with Weight Decay
  ######################################################  
  def step(self, step_size, momentum=0.9, weight_decay=0.0):
        self.velocity_weights = momentum * self.velocity_weights - step_size * (self.grad_weights + weight_decay * self.weights)
        self.velocity_bias = momentum * self.velocity_bias - step_size * (self.grad_bias + weight_decay * self.bias)
        self.weights += self.velocity_weights
        self.bias += self.velocity_bias



######################################################
# Q4 Implement Evaluation for Monitoring Training
###################################################### 

# TODO: Given a model, X/Y dataset, and batch size, return the average cross-entropy loss and accuracy over the set
def evaluate(model, X_val, Y_val, batch_size):
    losses = []
    accuracies = []
    
    num_examples = X_val.shape[0]
    
    for i in range(0, num_examples, batch_size):
        X_batch = X_val[i:i+batch_size]
        Y_batch = Y_val[i:i+batch_size]
        
        logits = model.forward(X_batch)
        
        loss_func = SigmoidCrossEntropy()
        loss = loss_func.forward(logits, Y_batch)
        losses.append(loss)
        
        predictions = (logits >= 0.5).astype(int)
        accuracy = np.mean(predictions == Y_batch)
        accuracies.append(accuracy)
    
    avg_loss = np.mean(losses)
    avg_accuracy = np.mean(accuracies)
    
    return avg_loss, avg_accuracy


def main():
    # Set optimization parameters
    batch_size = 64             #64,128,256
    max_epochs = 50
    
    step_size = 0.0001          #learning rate  0.01, 0.001, 0.0001  
    number_of_layers = 2
    width_of_layers = 100       #hidden layter 50,100,200
    weight_decay = 0.0001
    momentum = 0.8

    # Load data
    data = pickle.load(open('cifar_2class_py3.p', 'rb'))
    X_train = data['train_data'] / 255.0
    Y_train = data['train_labels']
    X_test = data['test_data'] / 255.0
    Y_test = data['test_labels']
    
    # Initialize lists for book-keeping
    losses = []
    val_losses = []
    accs = []
    val_accs = []
    
    # Get dimensions
    num_examples, input_dim = X_train.shape
    output_dim = 1  # Number of class labels, -1 for sigmoid loss

    # Build the network
    net = FeedForwardNeuralNetwork(input_dim, output_dim, width_of_layers, number_of_layers)
    
    # Q2 TODO: For each epoch below max epochs
    for epoch in range(max_epochs):
        epoch_avg_loss = 0.0
        epoch_total_acc = 0.0
        # Shuffle the training data
        permutation = np.random.permutation(num_examples)
        X_train_shuffled = X_train[permutation]
        Y_train_shuffled = Y_train[permutation]
        for i in range(0, num_examples, batch_size):
            # Get mini-batch
            X_batch = X_train_shuffled[i:i + batch_size]
            Y_batch = Y_train_shuffled[i:i + batch_size]
            # Forward pass
            logits = net.forward(X_batch)
            # Compute loss
            loss_func = SigmoidCrossEntropy()
            loss = loss_func.forward(logits, Y_batch)
            epoch_avg_loss += loss
            # Backward pass
            grad_loss = loss_func.backward(logits, Y_batch)
            net.backward(grad_loss)
            # Take optimizer step with momentum
            net.step(step_size, momentum, weight_decay)
            # Book-keeping for accuracy
            predictions = (logits >= 0.5).astype(int)
            accuracy = np.mean(predictions == Y_batch)
            epoch_total_acc += accuracy
        # Calculate average loss and accuracy for the epoch
        epoch_avg_loss /= (num_examples // batch_size)
        epoch_avg_acc = epoch_total_acc / (num_examples // batch_size)
        # Evaluate performance on test set after each epoch
        val_loss, val_acc = evaluate(net, X_test, Y_test, batch_size)
        val_accs.append(val_acc)
        # Add loss and accuracy to lists
        losses.append(epoch_avg_loss)
        accs.append(epoch_avg_acc)
        val_losses.append(val_loss)
        # Print training stats for each epoch
        print("[Epoch {:3}]   Loss: {:8.4f}   Train Acc: {:8.4f} Valid Acc: {:8.4f}".
              format(epoch + 1, epoch_avg_loss, epoch_avg_acc, val_acc))

    # Print some stats about the optimization process after each epoch
    logging.info("[Epoch {:3}]   Loss:  {:8.4}     Train Acc:  {:8.4}%      Val Acc:  {:8.4}%".
                 format(i, epoch_avg_loss, epoch_avg_acc, val_acc * 100))

    # Plot training and testing curves
    fig, ax1 = plt.subplots(figsize=(16, 9))
    color = 'tab:red'
    ax1.plot(range(len(losses)), losses, c=color, alpha=0.25, label="Train Loss")
    ax1.plot(range(len(val_losses)), val_losses, c="red", label="Val. Loss")
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Avg. Cross-Entropy Loss", c=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(-0.01, 3)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.plot(range(len(accs)), accs, c=color, label="Train Acc.", alpha=0.25)
    ax2.plot(range(len(val_accs)), val_accs, c="blue", label="Val. Acc.")
    ax2.set_ylabel("Accuracy", c=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(-0.01, 1.01)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax1.legend(loc="center")
    ax2.legend(loc="center right")
    plt.show()


#####################################################
# Feedforward Neural Network Structure
# -- Feel free to edit when tuning
#####################################################

class FeedForwardNeuralNetwork:

  def __init__(self, input_dim, output_dim, hidden_dim, num_layers):
   self.layers = []

   if num_layers == 1:
      self.layers = [LinearLayer(input_dim, output_dim)]
   else:
      self.layers.append(LinearLayer(input_dim, hidden_dim))
      self.layers.append(ReLU())
      for _ in range(num_layers - 2):
        self.layers.append(LinearLayer(hidden_dim, hidden_dim))
        self.layers.append(ReLU())
      self.layers.append(LinearLayer(hidden_dim, output_dim))

  def forward(self, X):
    for layer in self.layers:
      X = layer.forward(X)
    return X

  def backward(self, grad):
    for layer in reversed(self.layers):
      grad = layer.backward(grad)

  def step(self, step_size, momentum, weight_decay):
    for layer in self.layers:
      if hasattr(layer, 'step'):
          layer.step(step_size, momentum, weight_decay)



def displayExample(x):
  r = x[:1024].reshape(32,32)
  g = x[1024:2048].reshape(32,32)
  b = x[2048:].reshape(32,32)
  
  plt.imshow(np.stack([r,g,b],axis=2))
  plt.axis('off')
  plt.show()


if __name__=="__main__":
  main()