from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import numpy  as np
import tensorflow as tf

userpath = os.getenv("HOME")
COLIFORM_TRAINING = userpath + '/PycharmProjects/Germz/coliform_training.csv'

COLIFORM_TEST = '/PycharmProjects/Germz/coliform_test.csv'


class ColiformPrediction:
    def __init__(self):
        self.feature_columns = None

    def getDataResult(self, dataset):
        coliform_training_set, coliform_test_set = self.load_datasets()

        # Specify that all features have real-value data.
        self.feature_columns = [tf.feature_column.numeric_column("x", shape=[6])]

        # Build a 3 layer Deep Neural Network with 10, 20, 10 units respectively.
        classifier = self.build_model()

        # Define the training and testing inputs.
        coliform_train_input_fn, coliform_test_input_fn = self.define_inputs(coliform_training_set, coliform_test_set)

        # Train model.
        classifier.train(input_fn=coliform_train_input_fn, steps=2000)

        # Evaluate and print model accuracy.
        accuracy_score = classifier.evaluate(input_fn=coliform_test_input_fn)["accuracy"]

        # Define prediction function inputs.
        predict_input_fn = self.def_new_inputs(dataset)

        prediction = list(classifier.predict(input_fn=predict_input_fn))

        return prediction["classes"][0]

    def load_datasets(self):
        training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=COLIFORM_TRAINING,
            target_dtype=np.int,
            features_dtype=np.float32)
        test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=COLIFORM_TEST,
            target_dtype=np.int,
            features_dtype=np.float32)
        return training_set, test_set

    def build_model(self):
        model = tf.estimator.DNNClassifier(feature_columns=self.feature_columns,
                                           hidden_units=[10, 20, 10],
                                           n_classes=2,
                                           model_dir=userpath + "/tmp/coliform_model")
        return model

    def define_inputs(self, training_set, test_set):
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": np.array(training_set.data)},
            y=np.array(training_set.target),
            num_epochs=None,
            shuffle=True)

        test_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": np.array(test_set.data)},
            y=np.array(test_set.target),
            num_epochs=1,
            shuffle=False)
        return train_input_fn, test_input_fn

    def def_new_inputs(self, new_coliform_samples):
        input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": new_coliform_samples},
            num_epochs=1,
            shuffle=False)
        return input_fn
