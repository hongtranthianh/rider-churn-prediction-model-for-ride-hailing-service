# -*- coding: utf-8 -*-
"""modeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pg1TASAjaoK-F3MON5bcYkWLMjihZLso
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

new_df2 = pd.read_csv('new_df2.csv')
#new_df2['status'] = new_df2['status'].astype(str)

new_df2_nor = pd.read_csv('new_df2_nor.csv')
new_df2_nor['status'] = new_df2_nor['status'].astype(str)

#Separating the data into response and predictor variables
X = new_df2.iloc[:, :-1]
y = new_df2.iloc[:, -1]

X_nor = new_df2_nor.iloc[:, :-1]
y_nor = new_df2_nor.iloc[:, -1]

#DIVIDING THE DATA FOR TRAIN AND TEST SET
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y,\
                                                    test_size=0.2, shuffle = True, random_state = 1)

#DIVIDING THE NORMALIZED DATA FOR TRAIN AND TEST SET
X_train_nor, X_test_nor, y_train_nor, y_test_nor = train_test_split(X_nor, y_nor,\
                                                    test_size=0.2, shuffle = True, random_state = 1)

print('train set', X_train.shape, y_train.shape)
print('test set', X_test.shape, y_test.shape)

print('normalized train set', X_train_nor.shape, y_train_nor.shape)
print('normalized test set', X_test_nor.shape, y_test_nor.shape)

#FEATURE SELECTION (using ANOVA f-test)
#filter method
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

  #configure to select all features
fs = SelectKBest(score_func=f_classif, k='all')

  #learn relationship from the training set
fs.fit(X_train, y_train)

  #calculate scores for the features
for i in range(len(fs.scores_)):
	print('Feature %d: %f' % (i, fs.scores_[i]))
 
  #plot the scores
plt.bar([i for i in range(len(fs.scores_))], fs.scores_)
plt.show()

#select 12 best features from ANOVA f-test
'''  
 8   R_quantile               989 non-null    int64       
 0   Recency                  989 non-null    int64      
 11  RFM_score                989 non-null    float64     
 9   F_quantile               989 non-null    int64      
 10  M_quantile               989 non-null    int64      
 1   Frequency                989 non-null    int64  
 12  avg_rides_per_week       989 non-null    float64
 17  count_fail_trip          989 non-null    int64      
 14  start_type_asap          989 non-null    int64      
 2   Monetary                 989 non-null    int64      
 13  end_state_RiderCancel    989 non-null    int64      
 15  start_type_reserved      989 non-null    int64      
'''

from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from numpy import mean
from numpy import std
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

#Select k important features from ANOVA f-test
def select_features(X_train, y_train, X_test):
	fs = SelectKBest(score_func=f_classif, k=12)
	fs.fit(X_train, y_train)
	X_train_fs = fs.transform(X_train)
	X_test_fs = fs.transform(X_test)
	return X_train_fs, X_test_fs, fs
X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test)

#Select k important features from ANOVA f-test - using normalized data for SVM, LR and G-NB
def select_features(X_train_nor, y_train_nor, X_test_nor):
	fs = SelectKBest(score_func=f_classif, k=12)
	fs.fit(X_train_nor, y_train_nor)
	X_train_nor_fs = fs.transform(X_train_nor)
	X_test_nor_fs = fs.transform(X_test_nor)
	return X_train_nor_fs, X_test_nor_fs, fs
X_train_nor_fs, X_test_nor_fs, fs = select_features(X_train_nor, y_train_nor, X_test_nor)

#SVM
from sklearn import svm
  #TRAIN AND EVALUATE MODEL USING K-FOLD CROSS VALIDATION
    #cross validate the accuracy of model using above k selected features
cv = KFold(n_splits=10, random_state=1, shuffle=True)
model_SVM = svm.SVC(kernel='linear')
scores = cross_val_score(model_SVM, X_train_nor_fs, y_train_nor, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

#SVM
  #FINAL MODEL EVALUATION ON TEST SET
model_SVM.fit(X_train_nor_fs, y_train_nor)

y_pred_SVM = model_SVM.predict(X_test_nor_fs)

  #Summary of the predictions made by the model (classifier)
print(classification_report(y_test_nor, y_pred_SVM))
print(confusion_matrix(y_test_nor, y_pred_SVM))

  #Accuracy score
accuracy = accuracy_score(y_test_nor, y_pred_SVM)
print('Accuracy: %.2f' % (accuracy*100))

#LOGISTIC REGRESSION
from sklearn.linear_model import LogisticRegression
  #TRAIN AND EVALUATE MODEL USING K-FOLD CROSS VALIDATION
    #cross validate the accuracy of model using above k selected features
cv = KFold(n_splits=10, random_state=1, shuffle=True)
model_LR = LogisticRegression(solver='liblinear')
scores = cross_val_score(model_LR, X_train_nor_fs, y_train_nor, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

#LOGISTIC REGRESSION
  #FINAL MODEL EVALUATION ON TEST SET
model_LR.fit(X_train_nor_fs, y_train_nor)

y_pred_LR = model_LR.predict(X_test_nor_fs)

  #Summary of the predictions made by the model (classifier)
print(classification_report(y_test_nor, y_pred_LR))
print(confusion_matrix(y_test_nor, y_pred_LR))

  #Accuracy score
accuracy = accuracy_score(y_test_nor, y_pred_LR)
print('Accuracy: %.2f' % (accuracy*100))

#NAIVE BAYES
from sklearn.naive_bayes import GaussianNB
  #TRAIN AND EVALUATE MODEL USING K-FOLD CROSS VALIDATION
    #cross validate the accuracy of model using above k selected features
cv = KFold(n_splits=10, random_state=1, shuffle=True)
model_NB = GaussianNB()
scores = cross_val_score(model_LR, X_train_nor_fs, y_train_nor, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

#NAIVE BAYES
  #FINAL MODEL EVALUATION ON TEST SET
model_NB.fit(X_train_nor_fs, y_train_nor)

y_pred_NB = model_NB.predict(X_test_nor_fs)

  #Summary of the predictions made by the model (classifier)
print(classification_report(y_test_nor, y_pred_NB))
print(confusion_matrix(y_test_nor, y_pred_NB))

  #Accuracy score
accuracy = accuracy_score(y_test_nor, y_pred_NB)
print('Accuracy: %.2f' % (accuracy*100))

#FEATURE RANKING (SVM)
def f_importances(coef, names):
    imp = np.abs(coef)
    imp,names = zip(*sorted(zip(imp,names)))
    plt.barh(range(len(names)), imp, align='center')
    plt.yticks(range(len(names)), names)
    plt.title("Feature weights of SVM")
    plt.show()

features_names = ['R_quantile', 'Recency', 'RFM_score', 'F_quantile', 'M_quantile','Frequency',
                 'avg_rides_per_week', 'count_fail_trip', 'start_type_asap', 'Monetary',
                 'end_state_RiderCancel','start_type_reserved']

n_classes = 2
n_features = len(features_names)
f_importances(model_SVM.coef_.sum(axis=0), features_names)

#FEATURE RANKING (LOGISTIC REGRESSION)
def f_importances(coef, names):
    imp = np.abs(model_LR.coef_[0])
    imp,names = zip(*sorted(zip(imp,names)))
    plt.barh(range(len(names)), imp, align='center')
    plt.yticks(range(len(names)), names)
    plt.title("Feature weights of Logistic Regression")
    plt.show()
  
f_importances(model_LR.coef_.sum(axis=0), features_names)

from sklearn.inspection import permutation_importance

imps = permutation_importance(model_NB, X_train_nor_fs, y_train_nor)
importances = np.abs(imps.importances_mean)
std = imps.importances_std
indices = np.argsort(importances)[::1]

print("Feature ranking:")
for f in range(X_train_nor_fs.shape[1]):
    print("%d. %s (%f)" % (f + 1, features_names[indices[f]], importances[indices[f]]))

plt.title("Feature weights of Naive Bayes")
plt.barh(range(X_train_nor_fs.shape[1]), importances[indices], align="center")
plt.yticks(range(X_train_nor_fs.shape[1]), [features_names[indices[i]] for i in range(12)])
plt.ylim([-1, X_train_nor_fs.shape[1]])
plt.show()

#AFTER SELECT INPUT FEATURES FOR EACH MODEL

new_df2_nor_SVM = pd.read_csv('new_df2_nor_SVM.csv')
new_df2_nor_NB = pd.read_csv('new_df2_nor_NB.csv')
new_df2_nor_LR = pd.read_csv('new_df2_nor_LR.csv')

#Separating the data into response and predictor variables
X_nor_SVM = new_df2_nor_SVM.iloc[:, :-1]
y_nor_SVM = new_df2_nor_SVM.iloc[:, -1]

X_nor_NB = new_df2_nor_NB.iloc[:, :-1]
y_nor_NB = new_df2_nor_NB.iloc[:, -1]

X_nor_LR = new_df2_nor_LR.iloc[:, :-1]
y_nor_LR = new_df2_nor_LR.iloc[:, -1]

#DIVIDING THE DATA FOR TRAIN AND TEST SET
from sklearn.model_selection import train_test_split

X_train_SVM, X_test_SVM, y_train_SVM, y_test_SVM = train_test_split(X_nor_SVM, y_nor_SVM,\
                                                    test_size=0.2, shuffle = True, random_state = 1)

#DIVIDING THE NORMALIZED DATA FOR TRAIN AND TEST SET
X_train_NB, X_test_NB, y_train_NB, y_test_NB = train_test_split(X_nor_NB, y_nor_NB,\
                                                    test_size=0.2, shuffle = True, random_state = 1)

#DIVIDING THE NORMALIZED DATA FOR TRAIN AND TEST SET
X_train_LR, X_test_LR, y_train_LR, y_test_LR = train_test_split(X_nor_LR, y_nor_LR,\
                                                    test_size=0.2, shuffle = True, random_state = 1)


print('train set', X_train_SVM.shape, y_train_SVM.shape)
print('test set', X_test_SVM.shape, y_test_SVM.shape)

print('train set', X_train_NB.shape, y_train_NB.shape)
print('test set', X_test_NB.shape, y_test_NB.shape)

print('train set', X_train_LR.shape, y_train_LR.shape)
print('test set', X_test_LR.shape, y_test_LR.shape)

#SVM
scores = cross_val_score(model_SVM, X_train_SVM, y_train_SVM, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

model_SVM.fit(X_train_SVM, y_train_SVM)
y_pred_SVM = model_SVM.predict(X_test_SVM)

print(classification_report(y_test_SVM, y_pred_SVM))
print(confusion_matrix(y_test_SVM, y_pred_SVM))

accuracy = accuracy_score(y_test_SVM, y_pred_SVM)
print('Accuracy: %.2f' % (accuracy*100))

precision = precision_score(y_test_SVM, y_pred_SVM)
recall = recall_score(y_test_SVM, y_pred_SVM)
print('Precision: ',precision)
print('Recall: ',recall)
#Plotting Precision-Recall Curve
disp = plot_precision_recall_curve(model_SVM, X_test_SVM, y_test_SVM)

#Logistic Regression
scores = cross_val_score(model_LR, X_train_LR, y_train_LR, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

model_LR.fit(X_train_LR, y_train_LR)
y_pred_LR = model_LR.predict(X_test_LR)

print(classification_report(y_test_LR, y_pred_LR))
print(confusion_matrix(y_test_LR, y_pred_LR))

accuracy = accuracy_score(y_test_LR, y_pred_LR)
print('Accuracy: %.2f' % (accuracy*100))

precision = precision_score(y_test_LR, y_pred_LR)
recall = recall_score(y_test_LR, y_pred_LR)
print('Precision: ',precision)
print('Recall: ',recall)
#Plotting Precision-Recall Curve
disp = plot_precision_recall_curve(model_LR, X_test_LR, y_test_LR)

#Gaussian Naive Bayes
scores = cross_val_score(model_NB, X_train_NB, y_train_NB, scoring='accuracy', cv=cv, n_jobs=-1)
print('avg_accuracy: %.3f (%.3f)' % (mean(scores)*100, std(scores)))

model_NB.fit(X_train_NB, y_train_NB)
y_pred_NB = model_NB.predict(X_test_NB)

print(classification_report(y_test_NB, y_pred_NB))
print(confusion_matrix(y_test_NB, y_pred_NB))

accuracy = accuracy_score(y_test_NB, y_pred_NB)
print('Accuracy: %.2f' % (accuracy*100))

precision = precision_score(y_test_NB, y_pred_NB)
recall = recall_score(y_test_NB, y_pred_NB)
print('Precision: ',precision)
print('Recall: ',recall)
#Plotting Precision-Recall Curve
disp = plot_precision_recall_curve(model_NB, X_test_NB, y_test_NB)

#confusion matrix - SVM
conmat = confusion_matrix(y_test_SVM, y_pred_SVM)
val = np.mat(conmat) 
classnames = list(set(y_train_SVM))
df_cm = pd.DataFrame(val, index=classnames, columns=classnames)
#df_cm = (df_cm.astype('float') / df_cm.sum(axis=1)[:, np.newaxis])*100 

plt.figure()
heatmap = sns.heatmap(df_cm, annot=True, cmap="Blues")
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right')
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right')
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Churn SVM Model Results (%)')
plt.show()

#confusion matrix - LR
conmat = confusion_matrix(y_test_LR, y_pred_LR)
val = np.mat(conmat) 
classnames = list(set(y_train_LR))
df_cm = pd.DataFrame(val, index=classnames, columns=classnames)
df_cm = (df_cm.astype('float') / df_cm.sum(axis=1)[:, np.newaxis])*100  

plt.figure()
heatmap = sns.heatmap(df_cm, annot=True, cmap="Blues")
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right')
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right')
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Churn Logistic Regression Model Results (%)')
plt.show()

#confusion matrix - NB
conmat = confusion_matrix(y_test_NB, y_pred_NB)
val = np.mat(conmat) 
classnames = list(set(y_train_NB))
df_cm = pd.DataFrame(val, index=classnames, columns=classnames)
df_cm = (df_cm.astype('float') / df_cm.sum(axis=1)[:, np.newaxis])*100 

plt.figure()
heatmap = sns.heatmap(df_cm, annot=True, cmap="Blues")
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right')
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right')
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.title('Churn G-Naive Bayes Model Results (%)')
plt.show()

#plot lift chart for logistic gression
from sklearn import scikitplot as skplt
skplt.metrics.plot_cumulative_gain(y_test_LR, y_pred_LR)
plt.show()

