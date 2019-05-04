import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
from keras.regularizers import l2

def load_mnist_func(path):
    f = np.load(path)
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (x_train, y_train), (x_test, y_test)
(x_train_data,y_train_data),(x_test_data,y_test_data) = load_mnist_func(path='/home/peco/my_projects/TensorFlow_and_Keras_notes/Keras/mnist.npz')
print("x_train_shape:",x_train_data.shape)
print("y_train_shape:",y_train_data.shape)
print("x_test_shape:",x_test_data.shape)
print("x_test_shape:",y_test_data.shape)

#60000x28x28 ==>60000x784 并且归一化
x_train_data = x_train_data.reshape(x_train_data.shape[0],-1)/255.0
x_test_data = x_test_data.reshape(x_test_data.shape[0],-1)/255.0

# ==>onehot
y_train_data = np_utils.to_categorical(y_train_data,num_classes=10)
y_test_data = np_utils.to_categorical(y_test_data,num_classes=10)

#model 784==>200==>100=>10
model = Sequential([
    Dense(units=200,input_dim=784,bias_initializer='one',kernel_regularizer=l2(0.0003),activation='tanh'),
    Dropout(0.4),
    Dense(units=100,input_dim=200,bias_initializer='one',kernel_regularizer=l2(0.0003),activation='tanh'),
    Dropout(0.4),
    Dense(units=10,input_dim=100,bias_initializer='one',kernel_regularizer=l2(0.0003),activation='softmax'),
])
sgd = SGD(lr=0.1)
model.compile(
    optimizer=sgd,
    loss='categorical_crossentropy',
    metrics=['accuracy'])

#train
model.fit(x_train_data,y_train_data,batch_size=32,epochs=5)

#evaluate of test data
loss,accuracy = model.evaluate(x_test_data,y_test_data)
print("test loss: ",loss)
print("test acc: ",accuracy)

#evaluate of train data
loss,accuracy = model.evaluate(x_train_data,y_train_data)
print("train loss:",loss)
print("train loss:",accuracy)

def pred(name):
    img = cv.imread(name,0)
    img = cv.resize(img,(28,28),interpolation = 0)
    img = 255-img
    #plt.axis('off')
    #plt.imshow(img)
    data = cv.resize(img,(784,1))/255.0
    result = model.predict(data)
    print("pre result:",np.argmax(result,axis=1))
    return np.argmax(result,axis=1)

cnt = 0
for i in range(10):
    name = "/home/peco/my_projects/TensorFlow_and_Keras_notes/Keras/data/mnist_test_pictures/"+str(i)+".png"
    res = pred(name)
    if res  == i:
        cnt=cnt+1
print("test acc:",cnt/10.0)