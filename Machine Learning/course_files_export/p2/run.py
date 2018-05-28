from sklearn.tree import DecisionTreeClassifier
import multiclass
import util
import gd
import runClassifier
import linear
import mlGraphics
import datasets
from pylab import *
from datasets import *

x, trajectory = gd.gd(lambda x: 2*x**4-2*x**3-2*x**2+x, lambda x: 8*x**3-6*x**2-4*x+2, 0.8, 100, 0.1)
print("local:",x)
x, trajectory = gd.gd(lambda x: 2*x**4-2*x**3-2*x**2+x, lambda x: 8*x**3-6*x**2-4*x+2, -0.5, 100, 0.1)
print("global:",x)
