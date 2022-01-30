# -*- coding: utf-8 -*-
"""unisierraRNA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1espP5YUAG7fElldJwfBqpDE7mWINcC_B
"""

import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Dense
from keras.layers import Input
from keras.models import Model
from keras.models import Sequential
from keras.utils.vis_utils import plot_model
from pandas import read_csv
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
#from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

dataset = read_csv('https://raw.githubusercontent.com/aldojuarez/UNISIERRA-RNA/master/alumnos.csv')

dataset

le=LabelEncoder()
dataset.GENERO=le.fit_transform(dataset.GENERO)

dataset

y=dataset.iloc[:,-1].values
X=dataset.iloc[:,0:7].values

X.shape

y.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 1)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.25, random_state=1)

sc = StandardScaler(with_mean=False)

X_train_sc = sc.fit(X_train)
X_test_sc = sc.fit(X_test)

X_validation_sc = sc.fit(X_validation)
X_train = X_train_sc.transform(X_train)

X_test = X_test_sc.transform(X_test)
X_validation = X_validation_sc.transform(X_validation)

visible = Input(shape=(7,))
hidden1 = Dense(28, activation='sigmoid')(visible)
hidden2 = Dense(56, activation='sigmoid')(hidden1)
hidden3 = Dense(28, activation='sigmoid')(hidden2)
output = Dense(1, activation='sigmoid')(hidden3)
model = Model(inputs=visible, outputs=output)
print(model.summary())
plot_model(model, to_file='mlp_graph.png')

epochs = 10
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=epochs, verbose=False, validation_data=(X_validation, y_validation))

predictions = (model.predict(X_test) > 0.5).astype(int)
for i in range(20):
	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y_test[i]))
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.50)
cm = confusion_matrix(y_test, y_pred)
print(accuracy_score(y_test,y_pred)*100,'%')

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.50)
print(accuracy_score(y_test,y_pred)*100,'%')

plt.xlabel("Iteración/Época")
plt.ylabel("Precisión")
plt.plot(history.history["accuracy"])

plt.xlabel("Iteración/Época")
plt.ylabel("Historial de pérdida")
plt.plot(history.history["loss"])

epochsRange = range(0,epochs)
loss_train = history.history["accuracy"]
loss_val = history.history['val_accuracy']
plt.plot(epochsRange, loss_train, 'g', label='Precisión Entrenamiento ')
plt.plot(epochsRange, loss_val, 'b', label='Precisión Validación')
plt.title('Precisión de entrenamiento y validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

loss_train = history.history['loss']
loss_val = history.history['val_loss']
plt.plot(epochsRange, loss_train, 'g', label='Pérdida entrenamiento')
plt.plot(epochsRange, loss_val, 'b', label='Pérdida validación')
plt.title('Pérdida de entrenamiento y validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.show()

X, y = make_classification(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(
X, y, random_state=0)
clf = SVC(random_state=0)
clf.fit(X_train, y_train)
SVC(random_state=0)
ConfusionMatrixDisplay.from_estimator(
clf, X_test, y_test)
plt.show()