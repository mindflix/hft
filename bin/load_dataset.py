# Load the MNIST data
import gzip
import numpy as np
import theano
import theano.tensor as T
import pickle


def load_data_shared(filename="data/mnist.pkl.gz"):
    f = gzip.open(filename, 'rb')
    training_data, validation_data, test_data = pickle.load(
        f, encoding="latin1")
    f.close()

    def shared(data):
        """Placez les données dans des variables partagées. Cela permet à Theano de copier
        les données sur le GPU, si celui-ci est disponible.

        """
        shared_x = theano.shared(
            np.asarray(data[0], dtype=theano.config.floatX), borrow=True)
        shared_y = theano.shared(
            np.asarray(data[1], dtype=theano.config.floatX), borrow=True)
        return shared_x, T.cast(shared_y, "int32")
    return [shared(training_data), shared(validation_data), shared(test_data)]


train_set_x, train_set_y = load_data_shared()[0]

batch_size = 500    # size of the minibatch

data = train_set_x[2 * 500: 3 * 500]
label = train_set_y[2 * 500: 3 * 500]
