# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    #print "labels",self.legalLabels
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    #print "traiingi data ", trainingData
    #print "datum & keys", datum
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"

    # getting the variables
    self.trainingData = trainingData
    self.trainingLabels = trainingLabels
    self.validationData = validationData
    self.validationLabels = validationLabels
    self.kgrid = kgrid

    # creating variables necessary for parameter estimation

    self.lentrainingdata = len(trainingData)
   # print "training data size", self.trainingDataSize
   # print "training data ", trainingData
   # print "training label ", trainingLabels
    self.traininginstances = {}  # required for calculating P(Y)
    self.conditionalProb = {} # required for calculating  P(F_i|Y = y)

   # initializing the variable to match with the given labels
    for label in self.legalLabels:
      self.traininginstances[label] = util.Counter()
      self.conditionalProb[label] = {}

   # classifying the variables in the training data
    for i in range(len(trainingData)):
      variable = trainingData[i] # hold the count of features
      #print "variable:",variable

      variableLabel = trainingLabels[i]   # holds the variable label
      self.traininginstances[variableLabel]["TotalCount"] += 1  # getting the count of the variables

      for features in self.features:
     #   print "features",features
        self.traininginstances[variableLabel][features] += variable[features]  # matching the features with the variable

#calculating the smoothing factor
    bestofk = 0
    bestnumbofkcorrect = 0
    for k in kgrid:
      for label in self.legalLabels:
        for feature in self.features:
          self.conditionalProb[label][feature] = (self.traininginstances[label][feature] + k) / (1.0 + self.traininginstances[label]["TotalCount"] + 2*k)
     # to know whether this is a best K
      numofCorrect = 0
      #print "validdata count", len(validationData)
      for i in range(len(validationData)):
        guessedLabel = self.calculateLogJointProbabilities(validationData[i]).argMax()
        if(guessedLabel == validationLabels[i]):
          numofCorrect += 1
      if numofCorrect > bestnumbofkcorrect:
        bestofk = k
        bestnumbofkcorrect = numofCorrect
    #setting k to bestofk
      self.k = bestofk
      for label in self.legalLabels:
        for feature in self.features:
          self.conditionalProb[label][feature] = (self.traininginstances[label][feature] + self.k) / (1.0 + self.traininginstances[label]["TotalCount"] + 2*self.k)



        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
   # util.raiseNotDefined()
   # print "training data size", self.lentrainingdata


   # calculating the log values to avoid underflow

    for label in self.legalLabels:
      logProb = math.log(self.traininginstances[label]["TotalCount"] / (self.lentrainingdata + 0.0))
     # print "logprob", logProb
      for feature in self.features:
        if(datum[feature]):
          logProb += math.log(self.conditionalProb[label][feature])
        else:
          logProb += math.log(1 - self.conditionalProb[label][feature])
      logJoint[label] = logProb

    return logJoint



    ##return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds




