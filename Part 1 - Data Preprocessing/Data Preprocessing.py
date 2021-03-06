#Data Preprocessing

#1 Importing the libraries
import numpy as np #mathematical tools
import matplotlib.pyplot as plt #plot charts
import pandas as pd #manage datasets
import os
np.set_printoptions(threshold=np.nan) # To print all values of an array when entered <array_name> in the console

#Changing the main directory
os.chdir('C:\\Users\\Matheus\\Documents\\GitHub\\Machine-Learning-A-Z\\Part 1 - Data Preprocessing')

#2 Importing the dataset
dataset = pd.read_csv('Data.csv')

#Creating the Matrix of Features - Independent Variable Vector
X = dataset.iloc[:,:-1].values #iloc is for independent features
#Used [:,:-1] to remove the last column (Purchased)

#Creating the Matrix of Results- Dependent Variable Vector
Y = dataset.iloc[:,3].values

#3 Working with missing data
"""
In the dataset, we have missing data for Spain (age)
and for Germany (salary).
Ways to handle with this:
1- Remove the lines where are some missing data
    It's not so secure because we can find some crucial information
2- Take the mean of columns (most usual)
    Replace the missing information with the mean of all column's value
"""
from sklearn.preprocessing import Imputer #sklearn is a library for machine learning models and preprocess module contains a lot of classes, methods to preprocess any dataset
imputer = Imputer(missing_values='NaN', strategy="mean",axis=0)
imputer = imputer.fit(X[:,1:3]) # : to "catch" all the lines ; Columns 1 and 2 have missing data, so that's why 1:3 which 3 is not inclusive
X[:, 1:3] = imputer.transform(X[:, 1:3]) #transform method replace the missing data

#4 Categorical Data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder #class to create an encoder for labels ; an encoder change the named label for a numbered label
labelencoder_X = LabelEncoder()
X[:,0] = labelencoder_X.fit_transform(X[:,0]) #each country was encoded (number labeled)
#0 - France; 1 - Germany; 2 - Spain
#Machine Learning models can think 2>1>0, so Spain>Germany>France. Their numbers do not have a relation. Need to fix it

#Fix it with "Dummy Variables/Encoding" using OneHotEncoder class. Did this to make sure that the machine learning models do not attribute in order into the categorical variables
onehotencoder = OneHotEncoder(categorical_features=[0]) #0 is the column to OneHotEncode the categories
X = onehotencoder.fit_transform(X).toarray() #Will onehotencode X
#For Purchased column we only need to use a label encoder because the machine learning model will know that is a category without a order between the two.
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)

#5 Splitting the Dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=0) #test size means part of your dataset is going to be the test set and the other part is goint to be the training set. 0.2 is 20% and it is a good choice
#We have 10 observations so, with 0.2, 8 will be the training set and 2 will be the test set

#6 Feature Scaling - Put the variables in the same range/scale
"""
-Machine Learning models are based on Euclidean distance between two data points. sqrt((x2-x1)^2 + (y2-y1)^2)
-Age and salary have different scale

Two methods:
    1- Standadization
            x_stand = (x - mean(x))/standard deviation(x)
    2- Normalization
            x_norm = ((x - min(x))/(max(x) - min(x))
-Sometimes machine learning models aren't based on Euclidean distances but it's important to do features scaling because the algorithm will converge much faster. Decision trees for example
"""
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test) #do not need to fit X_test because it's already fitted to the training set
#Do we need to fit and transform the dummy variables?
    #It depends on how much you want to keep interpretation in your models.
#Do we need to apply feature scaling to Y (the dependent variable vector)
    #No in this case because the dependent variable is a CATEGORICAL VARIABLE and it's taking only two values.
