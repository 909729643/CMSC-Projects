# from numpy import *
# from matplotlib.pyplot import *
# import dr
# import util
# import datasets
#
# (X,Y) = datasets.loadDigits()
# (P,Z,evals) = dr.pca(X, 784)
# print(evals)
# normalized_evals = evals/sum(evals)
# eval_index = range(0, len(normalized_evals))
#
# plot(eval_index, normalized_evals)
# ylabel('eigenvalue')
# xlabel('eigenvalue index')
# title('Normalized Eigenvalues')
# savefig('normalized_eigenvalues.png')
#
# cumsum = cumsum(normalized_evals)
# print (np.argmax(cumsum > 0.9))
# print (np.argmax(cumsum > 0.95))
#
# util.drawDigits(Z.T[:50,:], arange(50))
# show(True)


from nn import NN, Relu, Linear, SquaredLoss
from utils import data_loader, acc, save_plot, loadMNIST, onehot
model = NN(Relu(), SquaredLoss(), hidden_layers=[128,128])
model.print_model()
x_train, label_train = loadMNIST('data/train-images.idx3-ubyte', 'data/train-labels.idx1-ubyte')
x_test, label_test = loadMNIST('data/t10k-images.idx3-ubyte', 'data/t10k-labels.idx1-ubyte')
y_train = onehot(label_train)
y_test = onehot(label_test)

model = NN(Relu(), SquaredLoss(), hidden_layers=[128, 128], input_d=784, output_d=10)
model.print_model()
training_data, dev_data = {"X":x_train, "Y":y_train}, {"X":x_test, "Y":y_test}
from run_nn import train_1pass
model, plot_dict = train_1pass(model, training_data, dev_data, learning_rate=1e-2, batch_size=64)