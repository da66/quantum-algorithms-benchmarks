from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Sampler
from qiskit.algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

from machine_learning.datasets.load_credit_risk_data import data_loading

#Load Data
train_data, test_data = data_loading()
X_train, y_train = train_data.iloc[:,0:len(train_data.columns)-1], train_data.iloc[:,len(train_data.columns)-1]
X_test, y_test = test_data.iloc[:,0:len(test_data.columns)-1], test_data.iloc[:,len(test_data.columns)-1]
# Constract Ansatz

num_features = len(X_train.columns)

feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
ansatz = RealAmplitudes(num_qubits=num_features, reps=3)

optimizer = COBYLA(maxiter=100)

vqc = VQC(
    quantum_instance=AerSimulator(method='matrix_product_state'),
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=optimizer,
)

vqc.fit(X_train.to_numpy(), y_train.to_numpy())

print('Train Score', vqc.score(X_train.to_numpy(), y_train.to_numpy()))
print('Test Score',  vqc.score(X_test.to_numpy(), y_test.to_numpy()))

print('Train Accuracy',accuracy_score(y_train.to_numpy(), vqc.predict(X_train.to_numpy())))
print('Test Accuracy',accuracy_score(y_test.to_numpy(), vqc.predict(X_test.to_numpy())))

