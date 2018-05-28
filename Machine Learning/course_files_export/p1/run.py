import util
import datasets
import binary
import dumbClassifiers
import runClassifier
import dt
import knn
import perceptron
from numpy import *
from pylab import *

# runClassifier.trainTestSet(dt.DT({'maxDepth': 1}), datasets.SentimentData)
# runClassifier.trainTestSet(dt.DT({'maxDepth': 3}), datasets.SentimentData)
# runClassifier.trainTestSet(dt.DT({'maxDepth': 5}), datasets.SentimentData)
curve = runClassifier.learningCurveSet(dt.DT({'maxDepth': 9}), datasets.SentimentData)
runClassifier.plotCurve('DT on Sentiment Data', curve)